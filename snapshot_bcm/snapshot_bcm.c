// MIT License
// Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>

#include <assert.h>

#include "bcm_host.h"
#include "snapshot_bcm/snapshot_bcm.h"

DISPMANX_MODEINFO_T snapshot_info;
DISPMANX_RESOURCE_HANDLE_T resource;
DISPMANX_DISPLAY_HANDLE_T display;
VC_RECT_T rect;
int pitch = 0;
int is_ambibulb_init = 0;

void snapshot_bcm_init()
{
    bcm_host_init();

    int screen = 0;
    display = vc_dispmanx_display_open(screen);

    int ret = vc_dispmanx_display_get_info(display, &snapshot_info);
    assert(ret == 0);

    pitch = ALIGN_UP(3 * snapshot_info.width, 32);

    uint32_t vc_image_ptr;
    resource = vc_dispmanx_resource_create(
        VC_IMAGE_RGB888,
        snapshot_info.width,
        snapshot_info.height,
        &vc_image_ptr);

    ret = vc_dispmanx_rect_set(&rect, 0, 0, snapshot_info.width, snapshot_info.height);
    assert(ret == 0);

    is_ambibulb_init = 1;
}

TSnapshot *snapshot_bcm_init_snapshot()
{
    assert(is_ambibulb_init == 1);

    TSnapshot *snapshot = malloc(sizeof(TSnapshot));
    snapshot->buffer = calloc(1, pitch * snapshot_info.height);
    assert(snapshot->buffer);
    snapshot->height = snapshot_info.height;
    snapshot->width = snapshot_info.width;
    snapshot->size = pitch * snapshot_info.height;
    return snapshot;
}

void snapshot_bcm_free_snapshot(TSnapshot *snapshot)
{
    free(snapshot->buffer);
    free(snapshot);
}

void snapshot_bcm_take_snapshot(TSnapshot *snapshot)
{
    int ret = vc_dispmanx_snapshot(display, resource, DISPMANX_NO_ROTATE);
    assert(ret == 0);

    ret = vc_dispmanx_resource_read_data(resource, &rect, snapshot->buffer, pitch);
    assert(ret == 0);
}

void snapshot_bcm_free()
{
    int ret = vc_dispmanx_resource_delete(resource);
    assert(ret == 0);

    ret = vc_dispmanx_display_close(display);
    assert(ret == 0);

    bcm_host_deinit();
    is_ambibulb_init = 0;
}
