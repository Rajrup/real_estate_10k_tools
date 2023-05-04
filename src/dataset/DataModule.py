from omegaconf import DictConfig
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader

from .DatasetPlaceholder import DatasetPlaceholder
from .ValidationWrapper import ValidationWrapper

DATASETS = {
    "placeholder": DatasetPlaceholder,
}


class DataModule(LightningDataModule):
    cfg: DictConfig

    def __init__(self, cfg: DictConfig):
        super().__init__()
        self.cfg = cfg

    def train_dataloader(self):
        return DataLoader(
            DATASETS[self.cfg.dataset.name](self.cfg.dataset, "train"),
            self.cfg.train.batch_size,
            shuffle=True,
            num_workers=self.cfg.train.num_workers,
        )

    def val_dataloader(self):
        return DataLoader(
            ValidationWrapper(
                DATASETS[self.cfg.dataset.name](self.cfg.dataset, "val"),
                1,
            ),
            self.cfg.val.batch_size,
            num_workers=self.cfg.val.num_workers,
        )

    def test_dataloader(self):
        return DataLoader(
            DATASETS[self.cfg.dataset.name](self.cfg.dataset, "test"),
            self.cfg.test.batch_size,
            num_workers=self.cfg.test.num_workers,
        )