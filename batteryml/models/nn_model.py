# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import abc
import copy
import torch
import random
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler

from tqdm import tqdm
from torch.utils.data.dataloader import DataLoader

from batteryml.data import DataBundle

from .base import BaseModel


def seed_worker(worker_id):
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)


class NNModel(BaseModel, nn.Module, abc.ABC):
    def __init__(self,
                 batch_size: int = 32,
                 epochs: int = 10000,
                 workspace: str = None,
                 evaluate_freq: int = 500,
                 checkpoint_freq: int = 1000,
                 train_batch_size: int = None,
                 test_batch_size: int = None,
                 lr: float = 1e-3,
                 learning_rate: float = None,
                 # Scheduler parameters
                 scheduler: str = 'none',
                 scheduler_params: dict = None,
                 # Early stopping parameters
                 early_stopping: bool = False,
                 early_stopping_patience: int = 20,
                 early_stopping_min_delta: float = 1e-4,
                 # Gradient clipping
                 gradient_clip_val: float = 0.0):
        nn.Module.__init__(self)
        BaseModel.__init__(self, workspace)
        self.train_epochs = epochs
        self.evaluate_freq = evaluate_freq
        if checkpoint_freq is None or checkpoint_freq == 'None':
            self.checkpoint_freq = None
        else:
            self.checkpoint_freq = min(checkpoint_freq, self.train_epochs)
        self.train_batch_size = train_batch_size or batch_size
        self.test_batch_size = test_batch_size or batch_size
        # Support both 'lr' and 'learning_rate' for flexibility
        self.lr = learning_rate if learning_rate is not None else lr

        # Scheduler config
        self.scheduler = scheduler
        self.scheduler_params = scheduler_params or {}

        # Early stopping config
        self.early_stopping = early_stopping
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_min_delta = early_stopping_min_delta

        # Gradient clipping config
        self.gradient_clip_val = gradient_clip_val

        # Training history (populated during fit)
        self._training_history = []

    @property
    def training_history(self):
        """Return the complete training history recorded during fit()."""
        return self._training_history

    def _build_scheduler(self, optimizer, steps_per_epoch):
        """Build a learning rate scheduler based on self.scheduler config."""
        name = self.scheduler.lower()
        params = self.scheduler_params

        if name == 'none':
            return None
        elif name == 'cosine':
            T_max = params.get('T_max', self.train_epochs)
            return lr_scheduler.CosineAnnealingLR(optimizer, T_max=T_max)
        elif name == 'step':
            step_size = params.get('step_size', 30)
            gamma = params.get('gamma', 0.1)
            return lr_scheduler.StepLR(
                optimizer, step_size=step_size, gamma=gamma)
        elif name == 'plateau':
            patience = params.get('patience', 10)
            factor = params.get('factor', 0.5)
            return lr_scheduler.ReduceLROnPlateau(
                optimizer, patience=patience, factor=factor)
        elif name == 'onecycle':
            max_lr = params.get('max_lr', self.lr)
            if steps_per_epoch <= 0:
                raise ValueError(
                    "OneCycleLR requires steps_per_epoch > 0. "
                    "Check that the training dataset is not empty.")
            return lr_scheduler.OneCycleLR(
                optimizer,
                max_lr=max_lr,
                epochs=self.train_epochs,
                steps_per_epoch=steps_per_epoch)
        else:
            raise ValueError(
                f"Unknown scheduler '{self.scheduler}'. "
                f"Supported: 'none', 'cosine', 'step', 'plateau', 'onecycle'")

    def fit(self,
            dataset: DataBundle,
            timestamp: str = None,
            seed: int = 0):
        self.train()
        train_data = dataset.train_data
        loader = DataLoader(
            train_data, self.train_batch_size,
            shuffle=True, worker_init_fn=seed_worker)
        # TODO: support customization of optimizers
        optimizer = optim.Adam(self.parameters(), lr=self.lr)

        # Build learning rate scheduler
        steps_per_epoch = len(loader)
        sched = self._build_scheduler(optimizer, steps_per_epoch)
        is_onecycle = self.scheduler.lower() == 'onecycle'
        is_plateau = self.scheduler.lower() == 'plateau'

        timestamp = timestamp or 'UnknownTime'

        # Early stopping state
        best_eval_loss = float('inf')
        epochs_without_improvement = 0
        best_state_dict = None

        # Reset training history
        self._training_history = []

        latest = None
        for epoch in tqdm(range(self.train_epochs), desc='Training'):
            self.train()
            epoch_loss_sum = 0.0
            epoch_loss_count = 0

            for batch in loader:
                loss = self.forward(**batch, return_loss=True)
                if torch.isinf(loss) or torch.isnan(loss):
                    reset_parameters(self)
                    optimizer = optim.Adam(self.parameters(), lr=self.lr)
                    sched = self._build_scheduler(
                        optimizer, steps_per_epoch)
                else:
                    optimizer.zero_grad()
                    loss.backward()

                    # Gradient clipping
                    if self.gradient_clip_val > 0:
                        nn.utils.clip_grad_norm_(
                            self.parameters(), self.gradient_clip_val)

                    optimizer.step()

                    # OneCycleLR steps per batch
                    if sched is not None and is_onecycle:
                        sched.step()

                    epoch_loss_sum += loss.item()
                    epoch_loss_count += 1

            # Per-epoch scheduler step (not for OneCycleLR or Plateau)
            if sched is not None and not is_onecycle and not is_plateau:
                sched.step()

            # Current learning rate
            current_lr = optimizer.param_groups[0]['lr']
            avg_epoch_loss = (
                epoch_loss_sum / epoch_loss_count
                if epoch_loss_count > 0 else float('nan'))

            # Record training history
            history_entry = {
                'epoch': epoch + 1,
                'loss': avg_epoch_loss,
                'learning_rate': current_lr,
                'best_loss': best_eval_loss,
                'epochs_without_improvement': epochs_without_improvement,
            }
            self._training_history.append(history_entry)

            if self.checkpoint_freq is not None and \
                    (epoch + 1) % self.checkpoint_freq == 0:
                filename = f'{timestamp}_seed_{seed}_epoch_{epoch+1}.ckpt'
                if self.workspace is not None:
                    self.dump_checkpoint(self.workspace / filename)
                    latest = self.workspace / filename

            if (epoch + 1) % self.evaluate_freq == 0:
                pred = self.predict(dataset)
                score = dataset.evaluate(pred, 'RMSE')
                print(f'[{epoch+1}/{self.train_epochs}] RMSE {score:.2f}'
                      f'  lr={current_lr:.2e}', flush=True)

                eval_loss = score

                # ReduceLROnPlateau steps on eval metric
                if sched is not None and is_plateau:
                    sched.step(eval_loss)

                # Early stopping check
                if self.early_stopping:
                    delta = self.early_stopping_min_delta
                    if eval_loss < best_eval_loss - delta:
                        best_eval_loss = eval_loss
                        epochs_without_improvement = 0
                        # Save best model state
                        best_state_dict = copy.deepcopy(self.state_dict())
                    else:
                        epochs_without_improvement += 1

                    patience = self.early_stopping_patience
                    if epochs_without_improvement >= patience:
                        print(
                            f'Early stopping at epoch {epoch+1}: '
                            f'no improvement for '
                            f'{epochs_without_improvement} evaluations.',
                            flush=True)
                        # Restore best model
                        if best_state_dict is not None:
                            self.load_state_dict(best_state_dict)
                        break

        if self.workspace is not None and latest is not None:
            self.link_latest_checkpoint(latest)

    @torch.no_grad()
    def predict(
        self, dataset: DataBundle, data_type: str = 'test',
    ) -> torch.Tensor:
        self.eval()
        if data_type == 'test':
            test_data = dataset.test_data
        else:
            test_data = dataset.train_data

        loader = DataLoader(
            test_data, self.test_batch_size,
            shuffle=False, worker_init_fn=seed_worker)
        predictions = torch.cat([self.forward(**batch) for batch in loader])
        return predictions

    def to(self, device: str):
        return nn.Module.to(self, device)

    def dump_checkpoint(self, path: str):
        torch.save(self.state_dict(), path)

    def load_checkpoint(self, path: str):
        self.load_state_dict(torch.load(path))


def reset_parameters(model):
    @torch.no_grad()
    def weight_reset(m):
        reset_parameters = getattr(m, "reset_parameters", None)
        if callable(reset_parameters):
            m.reset_parameters()

    model.apply(weight_reset)
