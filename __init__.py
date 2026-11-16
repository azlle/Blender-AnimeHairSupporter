# SPDX-License-Identifier: GPL-3.0-or-later
# Originally licensed under Apache-2.0: Copyright (C) 2017-2021 saidenka, relarar, Taremin and contributors
# Modified by Azlle in 2026 for Blender 5.2 compatibility. See COPYRIGHT for details.
# アドオンを読み込む時に最初にこのファイルが読み込まれます
import importlib
import inspect
import sys
import bpy

# アドオン情報
bl_info = {
    'name': "Anime Hair Supporter",
    'author': "saidenka, Taremin, Azlle",
    'version': (26, 11, 0),
    'blender': (5, 2, 0),
    'location': "3Dビュー > オブジェクトモード > サイドバー > ツール > アニメ髪支援パネル",
    'description': "",
    'warning': "",
    'doc_url': "https://github.com/azlle/Blender-AnimeHairSupporter",
    'tracker_url': "https://github.com/azlle/Blender-AnimeHairSupporter/issues",
    'category': "Tools"
}

# サブスクリプト群をインポート
module_names = [
    "_panel",
    "convert_edgemesh_to_curve",
    "convert_curve_to_edgemesh",
    "maincurve_activate",
    "maincurve_volume_up",
    "maincurve_volume_down",
    "maincurve_extra_deform",
    "maincurve_gradation_tilt",
    "maincurve_select",
    "maincurve_hide",
    "maincurve_set_resolution",
    "maincurve_set_order",
    "tapercurve_activate",
    "tapercurve_id_singlize",
    "tapercurve_change_type",
    "tapercurve_mirror",
    "tapercurve_relocation",
    "tapercurve_remove_alones",
    "tapercurve_select",
    "tapercurve_hide",
    "convert_curve_to_armature",
    "convert_curve_to_mesh",
]
namespace = {}
for name in module_names:
    fullname = '{}.{}.{}'.format(__package__, "lib", name)
    if fullname in sys.modules:
        namespace[name] = importlib.reload(sys.modules[fullname])
    else:
        namespace[name] = importlib.import_module(fullname)


# パネルの設定
class AHS_Props(bpy.types.PropertyGroup):
    maincurve_expand: bpy.props.BoolProperty(name="メインパネルを展開", default=True)
    tapercurve_expand: bpy.props.BoolProperty(name="テーパーパネルを展開", default=True)
    bevelcurve_expand: bpy.props.BoolProperty(name="ベベルパネルを展開", default=True)


# モジュールからクラスの取得
classes = [AHS_Props]
for module in module_names:
    for module_class in [obj for name, obj in inspect.getmembers(
            namespace[module]) if inspect.isclass(obj)]:
        classes.append(module_class)


# プラグインをインストールしたときの処理
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ahs_props = bpy.props.PointerProperty(type=AHS_Props)


# プラグインをアンインストールしたときの処理
def unregister():
    # Blender 5.0 以降、bpy.props で定義したプロパティは辞書アクセス (scene['ahs_props']) できないため
    # プロパティ定義そのものを削除する
    del bpy.types.Scene.ahs_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# 最初に実行される
if __name__ == '__main__':
    register()
