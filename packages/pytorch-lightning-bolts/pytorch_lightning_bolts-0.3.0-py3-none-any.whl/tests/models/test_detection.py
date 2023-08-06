import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader

from pl_bolts.datasets import DummyDetectionDataset
from pl_bolts.models.detection import FasterRCNN


def _collate_fn(batch):
    return tuple(zip(*batch))


def test_fasterrcnn():
    model = FasterRCNN()

    image = torch.rand(1, 3, 400, 400)
    model(image)


def test_fasterrcnn_train(tmpdir):
    model = FasterRCNN()

    train_dl = DataLoader(DummyDetectionDataset(), collate_fn=_collate_fn)
    valid_dl = DataLoader(DummyDetectionDataset(), collate_fn=_collate_fn)

    trainer = pl.Trainer(fast_dev_run=True, default_root_dir=tmpdir)
    trainer.fit(model, train_dataloader=train_dl, val_dataloaders=valid_dl)


def test_fasterrcnn_bbone_train(tmpdir):
    model = FasterRCNN(backbone="resnet18", fpn=True, pretrained_backbone=True)
    train_dl = DataLoader(DummyDetectionDataset(), collate_fn=_collate_fn)
    valid_dl = DataLoader(DummyDetectionDataset(), collate_fn=_collate_fn)

    trainer = pl.Trainer(fast_dev_run=True, default_root_dir=tmpdir)
    trainer.fit(model, train_dl, valid_dl)
