import csv
import os
from colors import *



class Recipe:
    def __init__(self, name, flavor=None, pumps: int=None, roast=None, shots: int=None, creamer=False, sugar=False, iced=False):
        self.name = name
        self.flavor = flavor
        self.pumps = pumps
        self.roast = roast
        self.shots = shots
        self.creamer = str(creamer).lower() in ('true','1')
        self.sugar = str(sugar).lower() in ('true','1')
        self.iced = str(iced).lower() in ('true','1')
    
    def list_recipe(self):
        return [
            self.name,
            self.flavor if self.flavor is not None else '',
            self.pumps if self.pumps is not None else '',
            self.roast if self.roast is not None else '',
            self.shots if self.shots is not None else '',
            self.creamer,
            self.sugar,
            self.iced
        ]
    
class Recipe_Manager:
    def __init__(self, filename="recipes.csv"):
        self.filename = filename
        self.recipes = []
        self.load_recipes()
        self.FIELDNAMES = [
        "name", "flavor", "pumps", "roast", "shots", "creamer", "sugar", "iced"
        ]

    def load_recipes(self):
        self.recipes = [] 
        if not os.path.exists(self.filename): 
            print(f"File '{self.filename}' not found. Creating new file....")
            return
    # open csv file (or create if nonexistent)
        with open(self.filename, mode='r', newline='', encoding='utf-8') as file: 
            reader = csv.reader(file)
            header = next(reader, None) # skip first row
            for row in reader:
                try:
                    recipe = Recipe(
                        name=row[0], 
                        flavor=row[1] or None, 
                        pumps=int(row[2]) if row[2].isdigit() else None, 
                        roast=row[3] or None, 
                        shots=int(row[4]) if row[4].isdigit() else None,
                        creamer=row[5], 
                        sugar=row[6], 
                        iced=row[7] or None
                        )
                    self.recipes.append(recipe) # add existing recipes from csv to self.recipes list 
                except IndexError:
                    continue

    def save_recipe(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.FIELDNAMES) # Write the header
                for recipe in self.recipes: # for each recipe in list
                    writer.writerow(recipe.list_recipe())  # write to recipe csv

    def new_recipe(self, recipe: Recipe):
        for existing in self.recipes:
            if existing.name.lower() == recipe.name.lower():
                print(f"ERROR: cannot add '{recipe.name}' (Duplicate name)")
                return
        self.recipes.append(recipe) # add recipe to self.recipes list from load_recipe
        self.save_recipe() # write to csv file
        print(f"Added '{green}{recipe.name}{default}'")


    def view_recipes(self, search_term=None): # view all and/or search 
        if not self.recipes: # if recipes empty
            print(f"No recipes loaded...")
            return
        found = False # -------------------------------------------------------------- NOTE: do I need this? 
        i = 1
        for recipe in self.recipes:
            display = f"{i}. {green}{recipe.name}{default}:"
            if search_term and search_term.lower() not in recipe.name.lower():
                continue  
            display += f" Flavor: {recipe.flavor or 'N/A'}, Pumps: {recipe.pumps or 'N/A'}, Roast: {recipe.roast or 'N/A'}, Shots: {recipe.shots or 0}, Creamer: {'no' if recipe.creamer is False else 'yes'}, Sugar: {'no' if recipe.sugar is False else 'yes'}, Iced: {'no' if recipe.iced is False else 'yes'}"
            print(display)
            found = True
            i += 1
        if search_term and not found: 
            print(f"No recipes found matching '{search_term}'.")

    def exact_match(self, search_term=None): # using only for making a coffee
        if not self.recipes:
            print(f"No recipes loaded...")
            return
        i = 1
        for recipe in self.recipes:
            if search_term and search_term.lower() != recipe.name.lower():
                continue  
            i += 1
            return [
                recipe.name,
                recipe.flavor if recipe.flavor is not None else '',
                recipe.pumps if recipe.pumps is not None else '',
                recipe.roast if recipe.roast is not None else '',
                recipe.shots if recipe.shots is not None else '',
                recipe.creamer,
                recipe.sugar,
                recipe.iced
            ]
            
    def list_names(self): # list of all recipe names (for reference when adding)
        name_lst = []
        for recipe in self.recipes:
            name_lst.append(recipe.name)
        return name_lst
    
    def del_recipe(self, index: int): 
        # self.view_recipes()
        try:
            removed_recipe = self.recipes.pop(index)
            self.save_recipe()
            print(f"Removed '{green}{removed_recipe.name}{default}'")
        except IndexError:
            print(f"Error: {index + 1} does not exist.")

    def list_flavors(self): # count pumps per flavor --- NOTE: maybe for tracking?? we'll see.... maybe will do recipe count instead of pump? idk
        flavor_lst = []
        for recipe in self.recipes:
            flavor = recipe.flavor
            if recipe.flavor and flavor not in flavor_lst:
                flavor_lst.append(flavor)
        return flavor_lst       

class User_Interaction:
    def __init__(self):
        self.main_options = [
            'View recipes',
            'Search for recipes',
            'Add new recipe',
            'Delete a recipe',
            'Make a coffee',
            'Exit'            
        ]
        self.add_details = [
            'Flavor', 
            'Pumps', 
            'Roast', 
            'Shots', 
            'Creamer (y/N)', 
            'Sugar (y/N)', 
            'Iced (y/N)'
        ]
        self.custom_details = [
            'Flavor', 
            'Pumps', 
            'Roast', 
            'Shots', 
            'Creamers', 
            'Sugars', 
            'Iced (y/N)'
        ]
     
    def main_menu(self): 
        menu_txt = "Main Menu"
        print(f"{borange}{menu_txt:^24}{default}\n------------------------")
        i = 1
        for opt in self.main_options:
            if opt == "Exit":
                print(f" {i}. {yellow}{opt}{default}")
            else:
                print(f" {i}. {opt}")
            i += 1

    def enter_new_name(self):    # ensure name is unique & not blank
        recipe = Recipe_Manager("recipes.csv") 
        name_Lst = recipe.list_names()
        name_lst = []
        for n in name_Lst:
            name_lst.append(n.lower())
        while True:
            entry = input(f"Please enter {teal}Name{default}: ")
            if not entry:
                print(f"ERROR: must provide a name")
                continue
            if entry.lower() in name_lst:
                print(f"ERROR: cannot add '{entry}' (Duplicate name)")
                continue
            return entry 
        
    def new_details(self, name):    # finish recipe details for adding
        recipe = Recipe_Manager("recipes.csv") 
    # receive user input
        while True:
            entry_lst = [name]            
            for i in self.add_details:
                entry = input(f"Please enter {teal}{i}{default}: ")
                if i == "Creamer (y/N)" or i == "Sugar (y/N)" or i == "Iced (y/N)":
                    entry = entry
                    if entry.lower() == "yes":
                        entry = True
                    elif entry.lower() == "y":
                        entry = True
                    elif entry.lower() == "true":
                        entry = True
                    elif entry.lower() == "t":
                        entry = True
                    else:
                        entry = False
                entry_lst.append(entry)
    # add to recipe file
            try:
                new = Recipe(
                    name=entry_lst[0], 
                    flavor=entry_lst[1] or None, 
                    pumps=int(entry_lst[2]) if entry_lst[2].isdigit() else None, 
                    roast=entry_lst[3] or None, 
                    shots=int(entry_lst[4]) if entry_lst[4].isdigit() else None,
                    creamer=entry_lst[5], 
                    sugar=entry_lst[6], 
                    iced=entry_lst[7]
                    )
            except ValueError as e:
                continue
            return new
        
    def new_custom(self, entry_lst):
        try:
                custom = Recipe(
                    name=entry_lst[0], 
                    flavor=entry_lst[1] or None, 
                    pumps=int(entry_lst[2]) if entry_lst[2].isdigit() else None, 
                    roast=entry_lst[3] or None, 
                    shots=int(entry_lst[4]) if entry_lst[4].isdigit() else None,
                    creamer=entry_lst[5], 
                    sugar=entry_lst[6], 
                    iced=entry_lst[7]
                    )
                    
        except ValueError as e:
            print("invalid recipe")
        return custom
        
    def select_recipe(self, matches):
        recipe = Recipe_Manager("recipes.csv")
        while True:
            try:
                choice_recipe = input(f"Please enter the number of the recipe you would like to make: ")
                choice_recipe == int(choice_recipe)
                choice_recipe = (int(choice_recipe) - 1) # index for consistency :)
                chosen_recipe = recipe.exact_match(matches[choice_recipe])
                if chosen_recipe:
                    return chosen_recipe
                else:
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
            except IndexError:
                print("Please make a valid selection.")
                continue

    def prepare_receipt(self,x,receipt_txt,chosen_recipe,size):
        # assign fields as floats for receipt
        if chosen_recipe[2] == '':
            pump = 0.0
        else:
            pump = float(chosen_recipe[2])
        if chosen_recipe[4] == '':
            shot = 0.0
        else:
            shot = float(chosen_recipe[4])
        creamer = 0.0
        sugar = 0.0
        if chosen_recipe[5] == True:
            creamer = 1.0
            creamer = creamer * size
            if "latte" in chosen_recipe[0].lower():
                creamer = creamer * 3 # lattes are basically just coffee milk :p
        if chosen_recipe[6] == True:
            sugar = 1.0
            sugar = sugar * size
        # price per
        size_price = 1.0
        pump_price = .25
        shot_price = .5
        creamer_price = .1
        sugar_price = .05
        # cost
        size_total = size * size_price
        pump_total = pump * pump_price
        shot_total = shot * shot_price
        creamer_total = creamer * creamer_price
        sugar_total = sugar * sugar_price
        # total
        subtotal = size_total + pump_total + shot_total + creamer_total + sugar_total

        if size == 1:
            size_str = "Sm"
        elif size == 2:
            size_str = "Med"
        elif size == 3:
            size_str = "Lg"
        elif size == 0:
            size_str = ""
        if chosen_recipe[0] == "Canceled":
            receipt_item = f"{red} {x}. {'-' * 34} {chosen_recipe[0]}{default}"
            receipt_txt = receipt_txt + f"{receipt_item:<58}\n"
        else:
            receipt_item = f" {x}. {green}{chosen_recipe[0]}{default} ({size_str})"
            receipt_txt = receipt_txt + f"{receipt_item:<58}{size_total:.2f}\n      {chosen_recipe[1]:<10}\t  Qty: {pump:.0f}    {pump_total:.2f}\n      {"espresso shots":<10}\t  Qty: {shot:.0f}    {shot_total:.2f}\n      {"cream":<10}\t  Qty: {creamer:.0f}    {creamer_total:.2f}\n      {"sugar":<10}\t  Qty: {sugar:.0f}    {sugar_total:.2f}\n\t\t\t\t\t  {orange}{subtotal:>5.2f}{default}\n"
        # return_lst = [receipt_txt, subtotal]
        # return return_lst
        return [
            receipt_txt,
            subtotal
        ]
        
        
    def print_receipt(self, txt, subtotal:float):
        title = f"Receipt"
        subtotal_txt = f"Subtotal:"
        tip = subtotal * .2
        tip_txt = f"20% Gratuity:"
        total = subtotal + tip
        total_txt = f"Total:"
        # print receipt main
        print(f"{borange}{title:^49}{default}")
        print("-" * 49)
        print(txt)
        # print total lines:
        print(f"{orange}{subtotal_txt:>33}{default}   {subtotal:.2f}")
        print(f"{orange}{tip_txt:>33}{default}   {tip:.2f}")
        print(f"{orange}{total_txt:>33}{default}{bold}{total:>14.2f}{default}")
        # print(txt)
        
    def main_nav(self, selection):      # handle user's input choice
        recipe = Recipe_Manager("recipes.csv")
        while True: 
        # option 1 - view recipes 
            if selection == 0: 
                menu_txt = "Recipes"
                print(f"{borange}{menu_txt:^125}{default}\n{'-' * 125}")
                recipe.view_recipes()
                return
        # option 2 - search 
            elif selection == 1: 
                search = input(f"Please enter the recipe name you are looking for: ")
                results_txt = f"Results for '{search}'"
                print(f"{borange}{results_txt:^125}{default}\n{'-' * 125}")
                recipe.view_recipes(search)
                again = input(f"Would you like to search for another: (y/{bteal}N{default}):")
                if again.lower() == "yes" or again.lower() == "y":
                    continue
                else: 
                    return
        # option 3 - add recipe
            elif selection == 2: 
                while True:
                    name = self.enter_new_name()
                    new = self.new_details(name)
                    recipe.new_recipe(new)
                    again = input(f"Would you like to add another? (y/{bteal}N{default}): ")
                    if again.lower() == "yes" or again.lower() == "y":
                        continue
                    else: 
                        return
        # option 4 - delete recipe
            elif selection == 3: 
                while True: 
                    recipe.view_recipes()
                    try: 
                        choice = input(f"Please enter the recipe number you would like to delete: ")
                        choice == int(choice)
                        choice = (int(choice) - 1) # index for consistency :)
                        chosen = recipe.recipes[choice].name
                        confirm = input(f"Are you sure you want to delete '{green}{chosen}{default}'? (y/{bteal}N{default}): ") 
                        if confirm.lower() == "yes" or confirm.lower() == "y":
                            recipe.del_recipe(choice)
                        else: 
                            print(f"Did not delete {chosen}")
                            continue       
                        again = input(f"Would you like to delete another? (y/{bteal}N{default}): ")
                        if again.lower() == "yes" or again.lower() == "y":
                            continue
                        else: 
                            return
                    except ValueError:
                        print(f"{choice} is not a valid option.")
        # option 5 - make coffee
            elif selection == 4:
                recipe = Recipe_Manager()
                flavors = recipe.list_flavors()
                x = 1 # for adding to receipt
                receipt_txt = "" # initializing receipt entries
                grand_total = 0 # for adding to the receipt
                while True:
                    print(f"------- {orange}Coffee flavors{default} -------")
                    print(f"  1. {teal}Any{default}")
                    print(f"  2. {teal}Custom{default}")
                    i = 3 # for listing flavors
                    for f in flavors:
                        print(f"{i:>3}. {pink}{f}{default}")
                        i += 1
                    print(f"{i:>3}. {yellow}Cancel{default}")
                    try:
                    # choose flavor to find recipes for
                        choice_flavor = input(f"What coffee flavor would you like? Please enter the number: ")
                        choice_flavor == int(choice_flavor) # ensure entry is integer
                        choice_flavor = int(choice_flavor)
                        if choice_flavor == 1: # if any option is chosen
                            menu_txt = f"All recipes"
                            print(f"{menu_txt:^31}\n------------------------------") 
                            i = 1
                            matches = []
                            for rec in recipe.recipes:
                                matches.append(rec.name)
                            for n in matches:
                                print(f"{i}. {green}{n}{default}")
                                i += 1             
                            chosen_recipe = self.select_recipe(matches)    
                        elif choice_flavor == 2: # if custom option is chosen                       
                            chosen_recipe = ["Custom coffee"]            
                            for c in self.custom_details:
                                entry = input(f"Please enter {c}: ")
                                if c == "Iced (y/N)":
                                    entry = entry
                                    if entry.lower() == "yes":
                                        entry = True
                                    elif entry.lower() == "y":
                                        entry = True
                                    elif entry.lower() == "true":
                                        entry = True
                                    elif entry.lower() == "t":
                                        entry = True
                                    else:
                                        entry = False
                                if c == "Creamers":
                                    if entry.isdigit() and int(entry) > 0:
                                        entry = int(entry)
                                    elif entry.lower() == "yes":
                                        entry = 1
                                    elif entry.lower() == "y":
                                        entry = 1
                                    elif entry.lower() == "true":
                                        entry = 1
                                    elif entry.lower() == "t":
                                        entry = 1
                                    else:
                                        entry = 0
                                    entry = int(entry)
                                if c == "Sugars":
                                    if entry.isdigit() and int(entry) > 0:
                                        entry = int(entry)
                                    elif entry.lower() == "yes":
                                        entry = 1
                                    elif entry.lower() == "y":
                                        entry = 1
                                    elif entry.lower() == "true":
                                        entry = 1
                                    elif entry.lower() == "t":
                                        entry = 1
                                    else:
                                        entry = 0
                                    entry = int(entry)
                                chosen_recipe.append(entry)
                            save = input(f"Would you like to save this recipe? (y/{bteal}N{default})")
                            if save.lower() == "yes" or save.lower() == "y":
                                new_name = self.enter_new_name()
                                chosen_recipe[0] = new_name
                                save_lst = chosen_recipe
                                if save_lst[5] > 0:
                                    save_lst[5] = True
                                else:
                                    save_lst[5] = False

                                if save_lst[6] > 0:
                                    save_lst[6] = True
                                else:
                                    save_lst[6] = False 
                                custom_new = self.new_custom(save_lst)
                                recipe.new_recipe(custom_new)                          
                            else:
                                print("Recipe not saved")
                            
                        
                        elif choice_flavor > 2 and choice_flavor < i:     
                            choice_flavor = choice_flavor -3 # for index & to account for first 2 options                    
                            chosen_flavor = flavors[choice_flavor]
                            menu_txt = f"Recipes using {chosen_flavor}"
                            print(f"{menu_txt:^31}\n------------------------------")
                            search_lst = []
                            for r in recipe.recipes: 
                                name = r.name
                                # name = name.lower()
                                if r.flavor == chosen_flavor: # if flavor matches flavor in list of recipes
                                    search_lst.append(name) # add name to search list
                            i = 1
                            matches = []
                            for s in search_lst: # for each name with that flavor
                                print(f"{i}. {green}{s}{default}") # print name 
                                search_result = recipe.exact_match(s)     
                                matches.append(search_result[0]) # add search result(s) to list
                                i += 1  
                            
                            chosen_recipe = self.select_recipe(matches) # select recipe from match list
                        else: # if exit or no option is chosen
                            self.print_receipt(receipt_txt, grand_total)
                            return
                            

                    # choose size
                        print(f"------- {orange}Sizes{default} -------")
                        print(f"1. Small (default)\n2. Medium\n3. Large \n4. {yellow}Go back{default}")
                        size = input(f"Please enter the size number you would like: ")
                        if size == "2":
                            size == 2
                        elif size.lower() == "m":
                            size = 2
                        elif size.lower() == "medium":
                            size = 2
                        elif size == "3":
                            size = 3
                        elif size.lower() == "l":
                            size = 3
                        elif size.lower() == "large":
                            size = 3
                        elif size == "4":
                            chosen_recipe = ['Canceled', '', 0, '', '', False, False, False]
                            size = 0
                        else:
                            size = 1
                        size == int(size) # ensure size is an integer
                        size = float(size) # change to float for math
                        print(size, chosen_recipe)
                        prepared_receipt = self.prepare_receipt(x, receipt_txt, chosen_recipe, size)
                        receipt_txt = prepared_receipt[0]
                        subtotal = prepared_receipt[1]
                        grand_total += subtotal
                        x += 1
                        again = input(f"Would you like to make another? ({bteal}Y{default}/n): ")
                        if again.lower() == "n" or again.lower() == "no":
                            self.print_receipt(receipt_txt, grand_total)            
                            return 
                        else:           
                            continue

                    except ValueError:
                        continue
                    except IndexError:
                        print("index error")
                    # except NameError:
                    #     print("name error")
            else: # exit -- shouldn't need this but whatever
                continue

def main():
    ui = User_Interaction()
    recipe = Recipe_Manager()
    while True:
        try:
            ui.main_menu()
            choice = input(f"Please enter the option number: ")
            choice = int(choice)
            if choice <= 0 or choice > 6: # if choice isn't an option
                print(f"{choice} is not valid")
            if choice == 6:
                break
            else:
                pass
            choice = choice - 1 # index for consistency :)
            
            ui.main_nav(choice)
            back = input(f"Return to main menu? ({bteal}Y{default}/n): ")
            if back.lower() == "n" or back.lower() == "no":
                break
            else:
                continue
                
        except ValueError:
            print(f"{choice} is not valid.")
            continue
    
if __name__ == '__main__':
    main()
