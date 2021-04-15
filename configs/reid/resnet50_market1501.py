# dataset settings
dataset_type = 'Market1501'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    #dict(type='RandomResizedCrop', size=224),
    dict(type='RandomFlip', flip_prob=0.5, direction='horizontal'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img']),
    dict(type='ToTensor', keys=['gt_label']),
    dict(type='Collect', keys=['img', 'gt_label'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    #dict(type='Resize', size=(256, -1)),
    #dict(type='CenterCrop', crop_size=224),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img']),
    dict(type='Collect', keys=['img'])
]
data = dict(
    samples_per_gpu=32,
    workers_per_gpu=2,
    triplet_sampler=False,
    train=dict(
        type=dataset_type,
        data_prefix='data/Market-1501-v15.09.15/bounding_box_train',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        data_prefix='data/Market-1501-v15.09.15/bounding_box_test',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        data_prefix='data/Market-1501-v15.09.15/bounding_box_test',
        pipeline=test_pipeline),
    )
evaluation = dict(interval=1, metric='accuracy')

# model settings
model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(3, ),
        style='pytorch'),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='BotHead',
        in_channels=2048,
        loss_ce=dict(type='CrossEntropyLoss', loss_weight=1.0),
        loss_tri=None,
    ))

#optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0001)
#optimizer = dict(type='Adam', lr=0.0003, momentum=0.9, weight_decay=0.0005)
optimizer = dict(type='Adam', lr=0.0003)
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(policy='step', step=[40, 90])
runner = dict(type='EpochBasedRunner', max_epochs=120)

# checkpoint saving
checkpoint_config = dict(interval=10)
# yapf:disable
log_config = dict(
    interval=100,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]