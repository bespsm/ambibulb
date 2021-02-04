// MIT License
// Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>

#pragma once

typedef struct
{
   unsigned int width;
   unsigned int height;
   unsigned int size;
   unsigned char *buffer;
} TSnapshot;

void snapshot_bcm_init();

TSnapshot *snapshot_bcm_init_snapshot();

void snapshot_bcm_free_snapshot(TSnapshot *snapshot);

void snapshot_bcm_take_snapshot(TSnapshot *snapshot);

void snapshot_bcm_free();
