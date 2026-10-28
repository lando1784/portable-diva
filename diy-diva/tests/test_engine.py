import json
import unittest
from pathlib import Path

from diy_diva import color, engine, model, render

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = json.loads((ROOT / "examples" / "avatar-esempio.json").read_text(encoding="utf-8"))


def rows(recipe):
    return {row["label"]: row for section in recipe["sections"] for row in section["rows"]}


class ModelTest(unittest.TestCase):
    def test_example_is_valid(self):
        self.assertEqual(model.validate(EXAMPLE), [])

    def test_example_matches_json_schema(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema non installato")
        schema = json.loads((ROOT / "schema" / "avatar.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(EXAMPLE, schema)

    def test_rejects_out_of_range_and_bad_colors(self):
        avatar = {"schema_version": "0.1", "name": "x", "face": {"eye_size": 1.5}, "hair": {"color": "rosso"}}
        errors = model.validate(avatar)
        self.assertEqual(len(errors), 2)


class ColorTest(unittest.TestCase):
    def test_lab_white_and_black(self):
        self.assertAlmostEqual(color.hex_to_lab("#ffffff")[0], 100, places=1)
        self.assertAlmostEqual(color.hex_to_lab("#000000")[0], 0, places=1)

    def test_nearest_swatch(self):
        palette = [{"value": "nero", "hex": "#101010"}, {"value": "rame", "hex": "#9a4a22"}]
        self.assertEqual(color.nearest("#8b3a1e", palette)["value"], "rame")


class EngineTest(unittest.TestCase):
    def test_every_adapter_renders(self):
        for game_id in engine.list_adapters():
            with self.subTest(game=game_id):
                adapter = engine.load_adapter(game_id)
                for section in adapter["sections"]:
                    for control in section["controls"]:
                        self.assertIn(control["type"], engine._CONTROLS)
                self.assertIn("##", render.to_markdown(engine.build_recipe(EXAMPLE, adapter)))

    def test_lineage_follows_preference(self):
        recipe = engine.build_recipe(EXAMPLE, engine.load_adapter("dragon-age-veilguard"))
        self.assertEqual(rows(recipe)["Stirpe"]["setting"], "Elfo")

    def test_slider_percent_and_range(self):
        avatar = {"name": "x", "face": {"eye_size": 0.7}}
        percent = engine._slider(avatar, {"label": "o", "from": "face.eye_size"})
        ranged = engine._slider(avatar, {"label": "o", "from": "face.eye_size", "min": -50, "max": 50})
        self.assertTrue(percent["setting"].startswith("≈70%"))
        self.assertTrue(ranged["setting"].startswith("20 "))

    def test_build_weights_are_normalised(self):
        recipe = engine.build_recipe(EXAMPLE, engine.load_adapter("dragon-age-veilguard"))
        self.assertEqual(rows(recipe)["Forma del corpo (triangolo)"]["setting"],
                         "magro 50%, muscoloso 40%, robusto 10%")

    def test_missing_traits_fall_back_to_default(self):
        recipe = engine.build_recipe({"name": "vuoto"}, engine.load_adapter("monster-hunter-wilds"))
        self.assertEqual(rows(recipe)["Altezza"]["setting"], engine.DEFAULT)

    def test_color_fallback_path(self):
        avatar = {"name": "x", "hair": {"color": "#222222"}}
        row = engine._color(avatar, {"label": "s", "from": ["brows.color", "hair.color"]})
        self.assertTrue(row["setting"].startswith("#222222"))

    def test_age_is_described_in_years(self):
        recipe = engine.build_recipe(EXAMPLE, engine.load_adapter("dragon-age-origins"))
        self.assertIn("circa 28 anni", rows(recipe)["Età / rughe"]["reason"])

    def test_checklist_lists_every_control(self):
        for game_id in engine.list_adapters():
            with self.subTest(game=game_id):
                adapter = engine.load_adapter(game_id)
                sheet = render.to_checklist(adapter)
                total = sum(len(s["controls"]) for s in adapter["sections"])
                self.assertEqual(sheet.count("- [ ] **"), total)


if __name__ == "__main__":
    unittest.main()
