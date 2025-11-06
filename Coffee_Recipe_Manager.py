import csv

class CoffeeRecipe:
    def __init__(self, name, roast, shots, water_oz, milk_or_creamer, sweetener, remarks):
        self.name = name
        self.roast = roast
        try:
            self.shots = int(shots)
        except ValueError:
            self.shots = 0
        try:
            self.water_oz = float(water_oz)
        except ValueError:
            self.water_oz = 0.05
        
        self.milk_or_creamer = milk_or_creamer
        self.sweetener = sweetener
        self.remarks = str(remarks).replace('\n', ' ').replace('\r', ' ')

    def to_dict(self):
        return {
            'Name': self.name,
            'Roast': self.roast,
            'Shots': self.shots,
            'Water_oz': self.water_oz,
            'Milk_or_Creamer': self.milk_or_creamer,
            'Sweetener': self.sweetener,
            'Remarks': self.remarks
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d.get('Name', ''),
            d.get('Roast', ''),
            d.get('Shots', '0'),
            d.get('Water_oz', '0.0'),
            d.get('Milk_or_Creamer', 'None'),
            d.get('Sweetener', 'None'),
            d.get('Remarks', '')
        )


class RecipeManager:
    def __init__(self, filename='coffee_recipes.csv'):
        self.filename = filename
        self.recipes = []
        self.load_recipes()

    def add_recipe(self):
        print("\n--- Add a New Coffee Recipe ---")
        name = input("Enter recipe name: ").strip()
        roast = input("Type of roast (Light/Medium/Dark): ").strip()
        try:
            shots = int(input("How many shots of coffee: "))
        except ValueError:
            print("Invalid number of shots. Setting to 0.")
            shots = 0
        try:
            water_oz = float(input("How many ounces of water: "))
        except ValueError:
            print("Invalid ounces of water. Setting to 0.")
            water_oz = 0.0

        milk_or_creamer = input("Would you like to add milk or creamer? (Yes/No): ").strip()
        sweetener = input("Would you like to add sweetener? (Yes/No): ").strip()
        remarks = input("Remarks (optional): ").strip().replace('\n', ' ').replace('\r', ' ')

        new_recipe = CoffeeRecipe(name, roast, shots, water_oz, milk_or_creamer, sweetener, remarks)
        self.recipes.append(new_recipe)
        self.save_recipes()
        print(f"\n✅ Recipe '{name}' added successfully!\n")

    def view_recipes(self):
        if not self.recipes:
            print("\nNo recipes found. Add one first!\n")
            return
        print("\n--- Stored Coffee Recipes ---")
        for i, recipe in enumerate(self.recipes, start=1):
            print(f"{i}. {recipe.name} ({recipe.roast} Roast)")
        print("")

    def view_recipe_details(self):
        if not self.recipes:
            print("\nNo recipes available.\n")
            return
        self.view_recipes()
        try:
            choice = int(input("Enter recipe number to view details: ")) - 1
            if choice < 0 or choice >= len(self.recipes):
                raise IndexError
            recipe = self.recipes[choice]
            print(f"\n--- {recipe.name} ---")
            print(f"Roast: {recipe.roast}")
            print(f"Shots: {recipe.shots}")
            print(f"Water: {recipe.water_oz} oz")
            print(f"Milk or Creamer: {recipe.milk_or_creamer}")
            print(f"Sweetener: {recipe.sweetener}")
            if recipe.remarks:
                print(f"Remarks: {recipe.remarks}")
            print("")
        except (IndexError, ValueError):
            print("Invalid selection.\n")

    def delete_recipe(self):
        if not self.recipes:
            print("\nNo recipes to delete.\n")
            return
        self.view_recipes()
        try:
            choice = int(input("Enter recipe number to delete: ")) - 1
            if choice < 0 or choice >= len(self.recipes):
                raise IndexError
            deleted = self.recipes.pop(choice)
            self.save_recipes()
            print(f"\n🗑️ Recipe '{deleted.name}' deleted successfully.\n")
        except (IndexError, ValueError):
            print("Invalid selection.\n")

    def save_recipes(self):
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        'Name',
                        'Roast',
                        'Shots',
                        'Water_oz',
                        'Milk_or_Creamer',
                        'Sweetener',
                        'Remarks'
                    ],
                    quoting=csv.QUOTE_ALL
                )
                writer.writeheader()
                for recipe in self.recipes:
                    writer.writerow(recipe.to_dict())
        except Exception as e:
            print(f"⚠️ Error saving recipes: {e}")

    def load_recipes(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row:  # skip empty rows
                        self.recipes.append(CoffeeRecipe.from_dict(row))
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️ Error loading recipes: {e}")

    def main_menu(self):
        while True:
            print("=== Coffee Recipe Manager ===")
            print("1. Add Recipe")
            print("2. View All Recipes")
            print("3. View Recipe Details")
            print("4. Delete Recipe")
            print("5. Exit")
            choice = input("Select an option: ").strip()
            if choice == '1':
                self.add_recipe()
            elif choice == '2':
                self.view_recipes()
            elif choice == '3':
                self.view_recipe_details()
            elif choice == '4':
                self.delete_recipe()
            elif choice == '5':
                print("\n☕ Goodbye! Enjoy your coffee!\n")
                break
            else:
                print("Invalid choice, please try again.\n")


if __name__ == '__main__':
    try:
        manager = RecipeManager()
        manager.main_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\n☕ Program exited safely. Goodbye!\n")
    except Exception as e:
        print(f"\n⚠️ Unexpected error: {e}\n")
