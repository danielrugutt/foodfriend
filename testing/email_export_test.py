import unittest
import ../RecipeService
import ../Database

class TestRecipeExport(unittest.TestCase):

    def test_invalid_recipe(self):
        """ Testing case 1 - recipe is invalid """
        response, code = RecipeService.export_recipe(999999, "email")
        self.assertEqual(response, "Recipe not found")

    def test_no_ingredients(self):
        RecipeBuilder
        response, code =

    def test_no_steps(self):

    def test_no_ingredients_or_steps(self):

    def test_normal_recipe(self):


    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()
