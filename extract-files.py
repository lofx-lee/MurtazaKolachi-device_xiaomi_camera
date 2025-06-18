#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
    'system/lib64/libmicampostproc_client.so': blob_fixup()
        .remove_needed('libhidltransport.so'),
    'system/lib64/libcamera_algoup_jni.xiaomi.so': (
        blob_fixup()
        .replace_needed('libgui.so', 'libgui-xiaomi.so')
        .add_needed('libbinder_shim.so')
        .add_needed('libgui_shim_miuicamera.so')
    ),
    'system/lib64/libcamera_mianode_jni.xiaomi.so': (
        blob_fixup()
        .replace_needed('libgui.so', 'libgui-xiaomi.so')
        .add_needed('libbinder_shim.so')
        .add_needed('libgui_shim_miuicamera.so')
    ),
    'system/lib64/libgui-xiaomi.so': (
        blob_fixup()
        .replace_needed('android.hardware.graphics.common-V4-ndk.so',
                        'android.hardware.graphics.common-V5-ndk.so')
        .add_needed('libbinder_shim.so')
    ),
}  # fmt: skip

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libgrallocutils',
    ): lib_fixup_remove,
}

namespace_imports = [
    'hardware/qcom-caf/common/libqti-perfd-client',
    'vendor/qcom/opensource/display',
    'vendor/xiaomi/apollo',
]

module = ExtractUtilsModule(
    'camera',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
