'''
KEY FEATURES

1. Multiple Screens and Full App Flow:

The app uses several screens: menu, instructions, avatar creation, weekly planning, meal builder, 
exercise planner, and the simulation screen. All of these screens are linked together and connect the data
and fundamental components of the game, which adds substantial complexity to the overall flow.

2. Multiple Avatars with Independent BMI + Body Metrics

Users can create several avatars, each with its own name, age, height, weight, sex, and BMI. Adjusting
body metrics only affects the currently selected avatar, and switching avatars instantly updates the display
to show that avatar's own stored metrics and BMI. (** How to test: On the avatar screen, press "Add", enter 
a name, and press "Enter". Use the "+/-" buttons to adjust metrics. These changes apply only to this avatar.
Then press "Look in archive" to select another avatar and observe that its metrics and BMI are different
and update independently. **)

3. Weekly Meal and Exercise Planning

Each day of the week stores breakfast, lunch, dinner, and an exercise routine. Users can add food items
to a plate, remove items from the plate, adjust serving amounts, view the serving amount currently selected,
see the food item's calories per serving, view the full plate (all items + servings + total kcal), and view
total daily kcal intake/burnt. Users can also add exercise sessions, adjust the duration of the exercise, 
and see how many kcal are burnt based on the exercise type and duration. A day turns green once all meals + 
exercise are confirmed.(** How to test: After confirming an avatar, press "Next Step". Select a day, press 
"Add Plate", choose a category, click an item to see kcal per serving, adjust servings, and press "Add 
to plate". Use "Remove from plate" to take items/servings off the plate. Press "View Plate" to see all items 
and total kcal. Turn on "Show Daily Info" to see the day's kcal intake and burnt. **)

4. Reusing Meals and Exercise for the Whole Week (BUILT IN GRADING SHORTCUT)

After confirming any meal or exercise routine, the user can apply it to all seven days with one click.
(** How to test: After confirming a plate, press "View Confirmed Plate", then "Set meal for week?". For 
exercise, confirm a routine, then press "Set routine for entire week?")

5. Weight and BMI Simulation

Once the week is fully planned (every meal and exercise routine confirmed for all 7 days), all
day boxes turn green and the "Confirm Week" button also turns green. Then, the app simulates
how the avatar's weight and BMI will change over 3, 6, or 12 months (your choice on time frame) given the 
same habits repeat. 

Note: After the simulation finishes (results are shown), the user clicks anywhere on the simulation screen,
and a short animation plays showing the avatar getting slimmer or heavier. LOL :)

'''

from cmu_graphics import *

# Classes

class Avatar:
    
    def __init__(self, name, age = None, sex = None, height = None, weight = None):
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height
        self.weight = weight
        self.bmi = None
        
    def updateBmi(self):
        if self.height is None or self.weight is None or self.height == 0:
            self.bmi = None
            return
        weightKg = self.weight / 2.205
        heightM = self.height * 0.0254
        rawBmi = weightKg / (heightM ** 2)
        sexFactor = 0
        if self.sex == 'male':
            sexFactor = -0.5
        elif self.sex == 'female':
            sexFactor = 0.5
        ageFactor = 0
        if self.age is not None and self.age > 30:
            ageFactor = 0.03 * (self.age - 30)
        self.bmi = rawBmi + sexFactor + ageFactor
        
    def displayAge(self):
        if self.age != None:
            return f'Age: {self.age} years old'
        else:
            return 'Age: ---'
            
    def getAvatarName(self):
        return self.name
        
    def displaySex(self):
        if self.sex != None:
            return f'Sex: {self.sex}'
        else:
            return 'Sex: ---'
        
    def displayWeight(self):
        if self.weight != None:
            return f'Weight: {self.weight} lbs'
        else:
            return 'Weight: ---'
        
    def displayHeight(self):
        if self.height != None:
            return f'Height: {self.height} inches'
        else:
            return 'Height: ---'
            
    def displayBmi(self):
        if self.bmi == None:
            return 'Adjust settings to calculate your BMI!'
        else:
            return f'BMI: {self.bmi}'
     
class FoodItem:
    
    def __init__(self, foodName, kcalPerServ, category):
        self.foodName = foodName
        self.kcalPerServ = kcalPerServ
        self.category = category
        
    def __eq__(self, other):
        if isinstance(other, FoodItem):
            return self.foodName == other.foodName and self.category == other.category
            
    def __hash__(self):
        return hash((self.foodName, self.category))
        
    def getkCalPerServ(self):
        return self.kcalPerServ
        
class Plate:
    
    def __init__(self):
        self.plate = dict()
        self.totalkCal = 0
        
    def addFoodItem(self, foodItem, servingNum):
        if foodItem not in self.plate:
            self.plate[foodItem] = servingNum
        else:
            self.plate[foodItem] += servingNum
        self.totalkCal += foodItem.kcalPerServ * servingNum
            
    def removeFoodItem(self, foodItem, servingNum):
        if foodItem in self.plate:
            if servingNum >= self.plate[foodItem]:
                self.totalkCal -= foodItem.kcalPerServ * self.plate[foodItem]
                self.plate.pop(foodItem)
            else:
                self.plate[foodItem] -= servingNum
                self.totalkCal -= foodItem.kcalPerServ * servingNum
                
        
    def displayPlate(self):
        return f'{len(self.plate)} items, {self.totalkCal} calories'
        
class ExerciseSession:
    
    def __init__(self, typeOf, duration, avatar):
        self.typeOf = typeOf
        self.duration = duration
        self.avatar = avatar
        
    def caloriesBurnt(self):
        if self.typeOf == 'weightlifting': baseRate = 5
        elif self.typeOf == 'running': baseRate = 7
        elif self.typeOf == 'swimming': baseRate = 12
        avatarWeight = self.avatar.weight * 0.453
        return baseRate * self.duration * round((avatarWeight / 50), 3)
        
class DayPlan:
    
    def __init__(self):
        self.dayPlan = {'breakfast': None, 'lunch': None, 'dinner': None, 'exercise sessions': []}
        
    def setPlate(self, plate, mealType):
        self.dayPlan[mealType] = plate
        
    def getPlate(self, mealType):
        return self.dayPlan[mealType]
        
    def addExercise(self, session):
        self.dayPlan['exercise sessions'].append(session)
        
    def getExercise(self):
        return self.dayPlan['exercise sessions']
        
    def setExerciseRoutine(self, exercises):
        self.dayPlan['exercise sessions'] = exercises
        
    def getDailyIntake(self):
        totalIntake = 0
        for component in self.dayPlan:
            if component != 'exercise sessions':
                if self.dayPlan[component] != None:
                    totalIntake += self.dayPlan[component].totalkCal
        return totalIntake
        
    def getDailyBurnt(self):
        totalBurn = 0
        for session in self.dayPlan['exercise sessions']:
            totalBurn += session.caloriesBurnt()
        return totalBurn
            
    def computeDailyCalorieBalance(self):
        return self.getDailyIntake() - self.getDailyBurnt()
        
    def isCompleteDay(self):
        if (self.dayPlan['breakfast'] is not None and self.dayPlan['lunch'] is not None and
            self.dayPlan['dinner'] is not None and len(self.dayPlan['exercise sessions']) > 0):
                return True
        else:
            return False
            
        
class WeekPlan:
    
    def __init__(self):
        self.week = {'Mon': DayPlan(), 'Tues': DayPlan(), 'Wed': DayPlan(), 'Thurs': DayPlan(), 
                     'Fri': DayPlan(), 'Sat': DayPlan(), 'Sun': DayPlan()}
                     
    def setDayPlan(self, day, dayPlan):
        self.week[day] = dayPlan
        
    def getDayPlan(self, day):
        return self.week[day]
                     
    def setMealPlate(self, day, plate, mealType):
        self.week[day].setPlate(plate, mealType)
        
    def getMealPlate(self, day, mealType):
        return self.week[day].getPlate(mealType)
        
    def addExercise(self, day, session):
        self.week[day].addExercise(session)
        
    def getExercises(self, day):
        return self.week[day].getExercise()
        
    def setSameRoutineForWeek(self, app, exercises):
        for day in self.week:
            dayPlan = self.week[day]
            dayPlan.setExerciseRoutine(exercises)
            app.isExerciseConfirmed[day] = True
            
    def setSamePlateForWeek(self, app, plate, mealType):
        for day in self.week:
            dayPlan = self.week[day]
            dayPlan.setPlate(plate, mealType)
            app.tempPlates = dict()
        
    def computeWeeklyTotals(self):
        totalIntake, totalBurn = 0, 0
        for day in self.week:
            dayPlan = self.week[day]
            if dayPlan != None:
                totalIntake += dayPlan.getDailyIntake()
                totalBurn += dayPlan.getDailyBurnt()
        return totalIntake, totalBurn
        
    def isDayComplete(self, day):
        if self.week[day].isCompleteDay(): return True
        else: return False
        
    def allDaysComplete(self):
        for day in self.week:
            if not self.week[day].isCompleteDay():
                return False
        return True
        
class SimulationConfig:
    
    def __init__(self, timeHorizon, weekPlan, avatar):
        self.timeHorizon = timeHorizon
        self.weekPlan = weekPlan
        self.avatar = avatar
        self.oldWeight = self.avatar.weight
        self.oldbmi = self.avatar.bmi
        
    def computeWeightChange(self):
        totalIntake, totalBurn = self.weekPlan.computeWeeklyTotals()
        weeklyNet = totalIntake - totalBurn
        if self.timeHorizon == 3: numOfWeeks = 13
        elif self.timeHorizon == 6: numOfWeeks = 26
        elif self.timeHorizon == 12: numOfWeeks = 52
        totalNetkCal = numOfWeeks * weeklyNet
        weightChange = totalNetkCal / 20000
        return weightChange
        
    def updateAvatarWeight(self):
        self.avatar.weight += self.computeWeightChange()
        
    def getOldBmi(self):
        return self.oldbmi
        
    def getOldWeight(self):
        return self.oldWeight
        
class SimulationResult:
    
    def __init__(self, simulation, avatar):
        self.simulation = simulation
        self.avatar = avatar
        self.simulation.updateAvatarWeight()
        self.avatar.updateBmi()
        
    def getWeightChange(self):
        return self.avatar.weight - self.simulation.getOldWeight()
        
    def getBmiChange(self):
        return self.avatar.bmi - self.simulation.getOldBmi()
        
    def showChangeInString(self):
        bmiChange = self.getBmiChange()
        weightChange = self.getWeightChange()
        if bmiChange == 0: bmiSign = 'same'
        elif bmiChange > 0: bmiSign = 'increased'
        else: bmiSign = 'decreased'
        if weightChange == 0: weightSign = 'same'
        elif weightChange > 0: weightSign = 'increased'
        else: weightSign = 'decreased'
        return (f'Your weight {weightSign} by {self.getWeightChange()},' +
                f'and your BMI {bmiSign} by {self.getBmiChange()}'
                )
               
    def showNewWeight(self):
        return f'Your new weight is {self.avatar.weight}'
        
    def showNewBmi(self):
        return f'Your new BMI is {self.avatar.bmi}'
        
class Button:
    
    def __init__(self, x, y, w, h, label, backgroundColor, borderColor, fontSize, align):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.fontSize = fontSize
        self.align = align
        
    def isClicked(self, mouseX, mouseY):
        left, right, top, bottom = hoverOrClick(self.x, self.y, self.w, self.h)
        return left < mouseX < right and top < mouseY < bottom
        
    def doesHover(self, mouseX, mouseY):
        left, right, top, bottom = hoverOrClick(self.x, self.y, self.w, self.h)
        return left < mouseX < right and top < mouseY < bottom
        
    def draw(self, app):
        drawRect(self.x, self.y, self.w, self.h, 
                 fill = self.backgroundColor, border = self.borderColor, align = self.align)
        drawLabel(self.label, self.x, self.y, size = self.fontSize, font = 'montserrat')
        
class AvatarCell:
    
    def __init__(self, x, y, w, h, index, name):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.index = index
        self.hover = False
        self.name = name
        
    def getName(self):
        return self.name
        
class FoodCell:

    def __init__(self, x, y, w, h, category, foodItem):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.category = category
        self.foodItem = foodItem
        self.backgroundColor = 'lightGray'
        
    def getFoodItem(self):
        return self.foodItem
        
    def foodCellisClicked(self, mouseX, mouseY):
        return self.x < mouseX < self.x + self.w and self.y < mouseY < self.y + self.h
        
    def foodCellDoesHover(self, mouseX, mouseY):
        return self.x < mouseX < self.x + self.w and self.y < mouseY < self.y + self.h 
        
# Helper Functions
        
def buildAvatarArchiveGrid(app):
    app.avatarCells = []
    cellW, cellH = 180, 140
    cols = 3
    startX = 300
    startY = 140
    paddingX = 60
    paddingY = 35
    for i in range(len(app.avatars)):
        name = app.namesList[i]
        row = i // cols
        col = i % cols
        x = startX + col * (cellW + paddingX)
        y = startY + row * (cellH + paddingY)
        app.avatarCells.append(AvatarCell(x, y, cellW, cellH, i, name))
        
def buildFoodCellGrid(app, category):
    cellW, cellH = 240, 105
    cols = 3
    startX = 180
    startY = 210
    paddingX, paddingY = 60, 35
    if app.selectedMealType == 'dinner' or app.selectedMealType == 'lunch':
        foodList = app.foodMenu[category]
    else:
        foodList = app.breakfastMenu[category]
    for i in range(len(foodList)):
        row = i // cols
        col = i % cols
        x = startX + col * (cellW + paddingX)
        y = startY + row * (cellH + paddingY)
        foodItem = foodList[i]
        app.foodCells.append(FoodCell(x, y, cellW, cellH, category, foodItem))
        
        
def hoverOrClick(x, y, w, h):
    left = x - w/2
    right = left + w
    top = y - h/2
    bottom = top + h
    return (left, right, top, bottom)
    
def hasConfirmedPlateForWeek(app, mealType):
    if mealType == 'breakfast' and app.hasConfirmPlateForWeekBeenPressedB:
        return True
    elif mealType == 'lunch' and app.hasConfirmPlateForWeekBeenPressedL:
        return True
    elif mealType == 'dinner' and app.hasConfirmPlateForWeekBeenPressedD:
        return True
    else:
        return False
        
def showExerciseInfo(app):
    if app.selectedExerciseType is not None:
        if app.selectedExerciseType == 'weightlifting':
            baseRate = 5
            avatarWeight = app.avatars[app.selectedAvatarIndex].weight * 0.453
            kCalsBurnt = baseRate * app.exerciseDuration * round((avatarWeight / 50), 3)
        elif app.selectedExerciseType == 'running':
            baseRate = 7
            avatarWeight = app.avatars[app.selectedAvatarIndex].weight * 0.453
            kCalsBurnt = baseRate * app.exerciseDuration * round((avatarWeight / 50), 3)
        elif app.selectedExerciseType == 'swimming':
            baseRate = 12
            avatarWeight = app.avatars[app.selectedAvatarIndex].weight * 0.453
            kCalsBurnt = baseRate * app.exerciseDuration * round((avatarWeight / 50), 3)
        drawLabel('kCals burnt depneding on duration:', 
                   1020, 50, size = 16, font = 'montserrat')
        drawLabel(f'{kCalsBurnt} kCals', 1020, 75, size = 16, font = 'montserrat')
        
########### Animations #############

# Screens

def drawMenuScreen(app):
    drawLabel('Build Your Healthy Life', 600, 175, size = 35, font = 'montserrat')
    for button in app.menuButtons:
        button.draw(app)
        
def drawInstructionsScreen(app):
    drawLabel('Read Carefully', 600, 170, size = 55, font = 'montserrat', fill = 'red', bold = True)
    drawLabel('1) Customize your avatar by inputting your body metrics (age, height, sex, weight).', 600, 300, size = 25, font = 'montserrat')
    drawLabel('2) Plan out your weekly habits - meal combos & exercise.', 600, 350, size = 25, font = 'montserrat')
    drawLabel('3) Simulate how your weight and BMI would change over time if', 600, 400, size = 25, font = 'montserrat')
    drawLabel('you repeated this exact weekly meal plan and exercise routine for a given time frame!', 600, 430, size = 25, font = 'montserrat')
    for button in app.instructionsButtons:
        button.draw(app)
    
def drawAvatarScreen(app):
    for button in app.avatarButtons:
        button.draw(app)
    if app.avatars == []:
        drawLabel('Age: ---', 165, 472.5, size = 20, font = 'montserrat')
        drawLabel('Height: ---', 165, 507.5, size = 20, font = 'montserrat')
        drawLabel('Sex: ---', 165, 542.5, size = 20, font = 'montserrat')
        drawLabel('Weight: ---', 165, 577.5, size = 20, font = 'montserrat')
        drawLabel('Your BMI:', 390, 52.5, size = 25, font = 'montserrat')
        drawLabel('Adjust settings to calculate your BMI!', 390, 105, size = 23, fill = 'red', font = 'montserrat')
    else:
        drawLabel(app.avatars[app.selectedAvatarIndex].displayAge(), 165, 472.5, size = 20, font = 'montserrat')
        drawLabel(app.avatars[app.selectedAvatarIndex].displayHeight(), 165, 507.5, size = 20, font = 'montserrat')
        drawLabel(app.avatars[app.selectedAvatarIndex].displaySex(), 165, 542.5, size = 20, font = 'montserrat')
        drawLabel(app.avatars[app.selectedAvatarIndex].displayWeight(), 165, 577.5, size = 20, font = 'montserrat')
        drawLabel(f'{app.avatars[app.selectedAvatarIndex].displayBmi()}', 390, 105, size = 23, fill = 'red', font = 'montserrat')
        drawLabel('Your BMI:', 390, 52.5, size = 25, font = 'montserrat')
        drawLabel(f'Avatar Name: {app.avatars[app.selectedAvatarIndex].getAvatarName()}', 
                  390, 155, size = 20, fill = 'royalBlue', font = 'montserrat')
        drawImage(app.imageUrls[app.selectedAvatarIndex][:-4] + f'{app.imageNums[app.selectedAvatarIndex]}' + '.png', 325, 200)
    drawLabel('Pick Sex:', 975, 43.75, size = 20, font = 'montserrat')
    drawLabel('Age Toggle:', 975, 210, size = 20, font = 'montserrat')
    drawLabel('Height Toggle:', 975, 385, size = 20, font = 'montserrat')
    drawLabel('Weight Toggle:', 975, 560, size = 20, font = 'montserrat')
    drawLabel('+1/-1', 970, 260, size = 16, font = 'montserrat')
    drawLabel('+10/-10', 970, 340, size = 16, font = 'montserrat')
    drawLabel('+1/-1', 970, 430, size = 16, font = 'montserrat')
    drawLabel('+5/-5', 970, 515, size = 16, font = 'montserrat')
    drawLabel('+1/-1', 970, 605, size = 16, font = 'montserrat')
    drawLabel('+10/-10', 970, 665, size = 16, font = 'montserrat')
    drawLabel('(must press before inputting body metrics)', 615, 525, font = 'montserrat', size = 10, fill = 'red')
    
    
def drawAvatarArchiveScreen(app):
    drawLabel('Choose your archived avatar!', 600, 61.25, size = 25, font = 'montserrat')
    for cell in app.avatarCells:
        if cell.hover: fillColor = 'lightYellow'
        else: fillColor = None
        if app.selectedAvatarIndex == cell.index: borderColor = 'red'
        else: borderColor = 'black'
        drawRect(cell.x, cell.y, cell.w, cell.h, fill=fillColor, border=borderColor)
        drawLabel(f'{cell.getName()}', cell.x + cell.w/2, cell.y + cell.h/2, size = 15, font = 'montserrat')
    for button in app.avatarArchiveButtons:
        button.draw(app)
    
def drawWeeklyScheduleScreen(app):
    for i, day in enumerate(app.days):
        x, y, w, h = app.dayCells[i]
        if app.weekPlan.allDaysComplete():
            fill = 'lightGreen'
        elif day == app.selectedDay:
            fill = 'red'
        elif app.weekPlan.isDayComplete(day):
            fill = 'lightGreen'
        elif i == app.dayHoverIndex and not app.weekPlan.isDayComplete(day) and day != app.selectedDay:
            fill = 'yellow'
        else:
            fill = 'lightGray'
        drawRect(x, y, w, h, fill = fill, border = 'black')
        drawLabel(day, x + w/2, y + h/2, size = 20, font = 'montserrat')
    baseY = 175
    rowGap = 87.5
    sections = [
        ('Breakfast', 'breakfast'),
        ('Lunch', 'lunch'),
        ('Dinner', 'dinner'),
        ('Exercise', 'exercise')
    ]
    for idx, (label, component) in enumerate(sections):
        rowY = baseY + idx * rowGap
        drawLabel(label, 240, rowY, size = 20, align = 'center', font = 'montserrat')
        if component == 'exercise':
            data = app.weekPlan.getExercises(app.selectedDay)
            btnLabel = 'Add Routine' if not app.isExerciseConfirmed[app.selectedDay] else 'View Confirmed Routine'
            app.weeklyScheduleButtons[component].label = btnLabel
            app.weeklyScheduleButtons[component].y = rowY
            app.weeklyScheduleButtons[component].draw(app)
            continue
        mainBtn = app.weeklyScheduleButtons[component]
        confirmedPlate = app.weekPlan.getMealPlate(app.selectedDay, component)
        if confirmedPlate is not None:
            mainBtn.label = 'View Confirmed Plate'
            mainBtn.y = rowY
            mainBtn.draw(app)
            continue
        key = (app.selectedDay, component)
        tempPlate = app.tempPlates.get(key, None)
        if tempPlate is not None and len(tempPlate.plate) > 0:
            mainBtn.label = 'Add Plate'
            mainBtn.y = rowY
            mainBtn.draw(app)
            viewBtn = app.weeklyScheduleButtons[f'appViewPlate_{component}']
            confirmBtn = app.weeklyScheduleButtons[f'appConfirmPlate_{component}']
            viewBtn.label = 'View Plate'
            confirmBtn.label = 'Confirm Plate'
            viewBtn.y = rowY - 20
            confirmBtn.y = rowY + 20
            viewBtn.draw(app)
            confirmBtn.draw(app)
            continue
        mainBtn.label = 'Add Plate'
        mainBtn.y = rowY
        mainBtn.draw(app)
        viewBtn = app.weeklyScheduleButtons[f'appViewPlate_{component}']
        confirmBtn = app.weeklyScheduleButtons[f'appConfirmPlate_{component}']
        viewBtn.label = ''
        confirmBtn.label = ''
        continue
    confirmBtn = app.weeklyScheduleButtons['confirm']
    if app.weekPlan.allDaysComplete():
        confirmBtn.backgroundColor = 'green'
    else:
        confirmBtn.backgroundColor = 'red'
    confirmBtn.draw(app)
    app.showOrHideDailyInfoButton.draw(app)
    if app.showDailyInfo:
        drawLabel(f'{app.weekPlan.getDayPlan(app.selectedDay).getDailyIntake()} kCals consumed', 150, 600, size = 16)
        drawLabel(f'{app.weekPlan.getDayPlan(app.selectedDay).getDailyBurnt()} kCals burnt', 150, 630, size = 16)
    if not app.isExerciseConfirmed[app.selectedDay] and len(app.weekPlan.getExercises(app.selectedDay)) > 0:
        app.exerciseRoutineConfirmButton.draw(app)
        app.exerciseRoutineViewButton.draw(app)
        
        
    
def drawCategoryScreen(app):
    for button in app.categoryButtons:
       button.draw(app)
    drawLabel('Choose category', 620, 87.5, size = 35, font = 'montserrat', fill = 'red')
        
def drawPlateBuilderScreen(app):
    drawLabel('Pick a Food Item', 630, 70, size = 35, font = 'montserrat', fill = 'red')
    for cell in app.foodCells:
        if cell.foodItem == app.foodItemSelected:
            border = 'red'
            drawLabel(f'Food Info: {app.foodItemSelected.getkCalPerServ()} kcals', 
                      350, 40, size = 16, font = 'montserrat')
            drawLabel('per serving', 350, 60, size = 16, font = 'montserrat')
        else:
            border = 'black'
        drawRect(cell.x, cell.y, cell.w, cell.h, fill = cell.backgroundColor, border = border)
        drawLabel(cell.foodItem.foodName, cell.x + cell.w/2, cell.y + cell.h/2, size = 14, font = 'montserrat')
    if app.isServingToggleButtonDrawn:
        drawLabel('Serving Amount', 360, 131.25, size = 16, font = 'montserrat')
        key = (app.selectedDay, app.selectedMealType)
        drawLabel(f'{app.tempServingNums[key]} servings', 360, 166.25, size = 16, font = 'montserrat')
        for button in app.plateBuilderButtons:
            button.draw(app)
    app.backPlateButton.draw(app)
    app.viewPlateFromBuilderButton.draw(app)
    
def drawExerciseRoutineScreen(app):
    drawLabel('Add Exercise Routine', 600, 87.5, size = 22, font = 'montserrat')
    for button in app.exerciseButtons:
        if app.selectedExerciseType == button.label:
            button.backgroundColor = 'yellow'
        button.draw(app)
    if app.selectedExerciseType is not None:
        drawLabel(f'Duration: {app.exerciseDuration} min', 600, 472.5, size = 16, font = 'montserrat')
        for button in app.exerciseToggleButtons:
            button.draw(app)
        app.exerciseRoutineAddButton.draw(app)
    app.exerciseRoutineBackButton.draw(app)
    app.viewExerciseFromRoutineButton.draw(app)
    showExerciseInfo(app)
    
# onAppStart(app)
    
def onAppStart(app):
    app.menuButtons = [
        Button(600, 350, 300, 35, 'Play', 'lightBlue', 'black', 20, 'center'),
        Button(600, 420, 300, 87.5, 'Instructions', 'lightBlue', 'black', 20, 'center')
    ]
    app.instructionsButtons = [Button(600, 612.5, 300, 87.5, 'Back to Main', 'wheat', 'black', 20, 'center')]
    app.avatars = []
    app.avatarCells = []
    app.selectedAvatarIndex = 0
    app.tempName = ''
    app.isTypingName = False
    app.isShfitHeld = False
    app.canCustomizeCharacter = False
    app.canConfirmCharacter = False
    app.avatarButtons = [
        Button(360, 647.5, 660, 52.5, 'Next step: Plan your weekly schedule', 'salmon', 
               'black', 20, 'center'),
        Button(585, 481.25, 300, 35, 'Look in archive', 'wheat', 'black', 20, 'center'),
        Button(585, 525, 300, 35, 'Add                                          ', 'wheat', 'black', 20, 'center'),
        Button(585, 568.75, 300, 35, 'Confirm', 'wheat', 'black', 20, 'center'),
        Button(900, 122.5, 90, 52.5, 'M', 'lightBlue', 'black', 20, 'center'),
        Button(1050, 122.5, 90, 52.5, 'F', 'pink', 'black', 20, 'center'),
        Button(900, 260, 40, 30, '+', 'lightGray', 'black', 25, 'center'),
        Button(900, 340, 40, 30, '+', 'lightGray', 'black', 25, 'center'),
        Button(900, 430, 40, 30, '+', 'lightGray', 'black', 25, 'center'),
        Button(900, 515, 40, 30, '+', 'lightGray', 'black', 25, 'center'),
        Button(900, 605, 40, 30, '+', 'lightGray', 'black', 25, 'center'),
        Button(900, 665, 40, 30, '+', 'lightGray', 'black', 25, 'center'),
        Button(1050, 260, 40, 30, '-', 'lightGray', 'black', 25, 'center'),
        Button(1050, 340, 40, 30, '-', 'lightGray', 'black', 25, 'center'),
        Button(1050, 430, 40, 30, '-', 'lightGray', 'black', 25, 'center'),
        Button(1050, 515, 40, 30, '-', 'lightGray', 'black', 25, 'center'),
        Button(1050, 605, 40, 30, '-', 'lightGray', 'black', 25, 'center'),
        Button(1050, 665, 40, 30, '-', 'lightGray', 'black', 25, 'center'),
    ]
    app.imageUrls = [
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        'https://raw.githubusercontent.com/CalebOuyang/15112finalProj/master/person.png',
        
    ]
    app.imageNums = dict()
    app.showBodyImageChange = False
    app.avatarArchiveButtons = [
        Button(90, 630, 120, 52.5, 'Back', 'wheat', 'black', 12, 'center')
    ]
    app.namesList = []
    app.foodMenu = {
        'Carbs': [
            FoodItem('Brown Rice with Olive Oil', 150, 'Carbs'), 
            FoodItem('Quinoa Pilaf', 180, 'Carbs'),
            FoodItem('Butter Baked Potato', 220, 'Carbs'),
            FoodItem('Whole Wheat Bread Slice', 90, 'Carbs'),
            FoodItem('Sweet Potato Fries', 160, 'Carbs'),
            FoodItem('Steamed Jasmine Rice', 190, 'Carbs'),
            FoodItem('Herb Roasted Potatoes', 140, 'Carbs'),
            FoodItem('Mac and Cheese', 310, 'Carbs'),
            FoodItem('Spaghetti', 360, 'Carbs')
        ],
        'Protein': [
            FoodItem('Garlic-Butter Filet Mignon', 250, 'Protein'), 
            FoodItem('Marinated Flank Steak', 360, 'Protein'),
            FoodItem('Grilled Chicken Breast', 200, 'Protein'),
            FoodItem('Honey-Glazed Salmon', 280, 'Protein'),
            FoodItem('Lemon Garlic Shrimp', 160, 'Protein'),
            FoodItem('Turkey Meatballs', 220, 'Protein'),
            FoodItem('Pork Loin', 300, 'Protein'),
            FoodItem('BBQ Pulled Chicken', 250, 'Protein'),
            FoodItem('Teriyaki Tofu Cubes', 150, 'Protein'),
        ],
        'Veggies': [
            FoodItem('Roasted Broccoli', 35, 'Veggies'), 
            FoodItem('Mashed Potatoes', 45, 'Veggies'),
            FoodItem('Steamed Green Beans', 70, 'Veggies'),
            FoodItem('Mixed Garden Salad', 80, 'Veggies'),
            FoodItem('Satuéed Spinach', 60, 'Veggies'),
            FoodItem('Glazed Carrots', 110, 'Veggies'),
            FoodItem('Grilled Asparagus', 95, 'Veggies'),
            FoodItem('Caesar Salad Cup', 80, 'Veggies'),
            FoodItem('Roasted Brussels Sprouts', 95, 'Veggies')
        ],
        'Beverages': [
            FoodItem('Strawberry Lemonade', 50, 'Beverage'), 
            FoodItem('Iced Tea', 100, 'Beverage'),
            FoodItem('Water', 0, 'Beverage'),
            FoodItem('Orange Juice', 110, 'Beverage'),
            FoodItem('Apple Juice', 120, 'Beverage'),
            FoodItem('Sparkling Water', 0, 'Beverage'),
            FoodItem('Chocolate Milk', 140, 'Beverage'),
            FoodItem('Hot Green Tea', 20, 'Beverage'),
            FoodItem('Vanilla Shake', 250, 'Beverage'),
        ]
    }
    app.breakfastMenu = {
        'Carbs': [
            FoodItem('Oatemeal with Honey', 150, 'Carbs'), 
            FoodItem('Whole Wheat Toast', 90, 'Carbs'),
            FoodItem('Blueberry Pancakes', 220, 'Carbs'),
            FoodItem('Bananna Muffin', 180, 'Carbs'),
            FoodItem('Granola Cup', 200, 'Carbs'),
            FoodItem('Hash Browns', 160, 'Carbs'),
            FoodItem('Bagel', 250, 'Carbs'),
            FoodItem('Waffles with Syrup', 260, 'Carbs'),
            FoodItem('Breakfast Potatoes', 140, 'Carbs')
        ],
        'Protein': [
            FoodItem('Scrambled Eggs', 140, 'Protein'), 
            FoodItem('Hard-Boiled Eggs', 120, 'Protein'),
            FoodItem('Turkey Sausage Links', 160, 'Protein'),
            FoodItem('Griled Ham Slices', 130, 'Protein'),
            FoodItem('Greek Yogurt Cup', 100, 'Protein'),
            FoodItem('Cottage Cheese Bowl', 110, 'Protein'),
            FoodItem('Smoked Salmon Slices', 180, 'Protein'),
            FoodItem('Tofu Scrambles', 150, 'Protein'),
            FoodItem('Bacon Strips', 190, 'Protein'),
        ],
        'Veggies': [
            FoodItem('Satuéed Spinach', 40, 'Veggies'), 
            FoodItem('Grilled Tomatoes', 35, 'Veggies'),
            FoodItem('Avocado Slices', 80, 'Veggies'),
            FoodItem('Mixed Veggie Omelette', 60, 'Veggies'),
            FoodItem('Satuéed Mushrooms', 45, 'Veggies'),
            FoodItem('Bell Pepper Strips', 30, 'Veggies'),
            FoodItem('Kale Salad Cup', 55, 'Veggies'),
            FoodItem('Cucumber Slices', 25, 'Veggies'),
            FoodItem('Roastsed Zucchini', 70, 'Veggies')
        ],
        'Beverages': [
            FoodItem('Iced Coffee', 80, 'Beverage'), 
            FoodItem('Milk 2%', 100, 'Beverage'),
            FoodItem('Water', 0, 'Beverage'),
            FoodItem('Orange Juice', 110, 'Beverage'),
            FoodItem('Apple Juice', 120, 'Beverage'),
            FoodItem('Chocloate Milk', 140, 'Beverage'),
            FoodItem('Hot Green Tea', 20, 'Beverage'),
            FoodItem('Vanilla Shake', 250, 'Beverage'),
            FoodItem('Matcha', 180, 'Beverage')
        ]
    }
    app.weekPlan = WeekPlan()
    app.selectedDay = 'Mon'
    app.days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    app.dayCellHeight = 55
    app.dayListTopY = 55
    app.weeklyScheduleButtons = {
        'breakfast': Button(750, 175, 300, 52.5, 'Add Plate', 'lightGray', 'black', 20, 'center'),
        'lunch': Button(750, 262.5, 300, 52.5, 'Add Plate', 'lightGray', 'black', 20, 'center'),
        'dinner': Button(750, 350, 300, 52.5, 'Add Plate', 'lightGray', 'black', 20, 'center'),
        'exercise': Button(750, 437.5, 300, 52.5, 'Add Exercise', 'lightGray', 'black', 20, 'center'),
        'confirm': Button(750, 577.5, 300, 61.25, 'Confirm Week', 'lightGray', 'black', 20, 'center'),
        'appViewPlate_breakfast': Button(1050, 175, 180, 40, 'View Plate', 'wheat', 'black', 14, 'center'),
        'appConfirmPlate_breakfast': Button(1050, 215, 180, 40, 'Confirm Plate', 'lightGreen', 'black', 14, 'center'),
        'appViewPlate_lunch': Button(1050, 262.5, 180, 40, 'View Plate', 'wheat', 'black', 14, 'center'),
        'appConfirmPlate_lunch': Button(1050, 302.5, 180, 40, 'Confirm Plate', 'lightGreen', 'black', 14, 'center'),
        'appViewPlate_dinner': Button(1050, 350, 180, 40, 'View Plate', 'wheat', 'black', 14, 'center'),
        'appConfirmPlate_dinner': Button(1050, 390, 180, 40, 'Confirm Plate', 'lightGreen', 'black', 14, 'center')
        }
    app.showDailyInfo = False
    app.showOrHideDailyInfoButton = Button(150, 550, 150, 50, 'Show Daily Info', 'lightGray', 'black', 16, 'center')
    app.dayHoverIndex = None
    app.dayCells = [
        (30, 35, 150, 70),
        (195, 35, 150, 70),
        (360, 35, 150, 70),
        (525, 35, 150, 70),
        (690, 35, 150, 70),
        (855, 35, 150, 70),
        (1020, 35, 150, 70)
        ]
    app.selectedMealType = None
    app.selectedCategory = None
    app.categoryButtons = [
        Button(390, 245, 360, 140, 'Protein', 'lightGray', 'black', 25, 'center'),
        Button(810, 245, 360, 140, 'Carbs', 'lightGray', 'black', 25, 'center'),
        Button(390, 420, 360, 140, 'Veggies', 'lightGray', 'black', 25, 'center'),
        Button(810, 420, 360, 140, 'Beverages', 'lightGray', 'black', 25, 'center'),
        Button(120, 70, 150, 52.5, 'Back', 'wheat', 'black', 15, 'center'),
        Button(120, 595, 180, 52.5, 'View Plate', 'wheat', 'black', 15, 'center')
    ]
    app.foodCells = []
    app.foodItemSelected = None
    app.isServingToggleButtonDrawn = False
    app.plateBuilderButtons = [
        Button(600, 148.75, 90, 52.5, '+', 'lightGray', 'black', 20, 'center'),
        Button(750, 148.75, 90, 52.5, '-', 'lightGray', 'black', 20, 'center'),
        Button(1000, 45, 240, 50, 'Add to plate', 'red', 'black', 16, 'center'),
        Button(1000, 115, 240, 50, 'Remove from plate', 'orange', 'black', 16, 'center')
    ]
    app.viewPlateFromBuilderButton = Button(120, 645, 180, 52.5, 'View Plate', 'wheat', 'black', 14, 'center')
    app.backPlateButton = Button(120, 70, 150, 43.75, 'Back', 'wheat', 'black', 12, 'center')
    app.setPlateForWeekButton = Button(120, 140, 180, 60, 'Set meal for week?',
                                       'orange', 'black', 12, 'center')
    app.hasConfirmPlateForWeekBeenPressedB = False
    app.hasConfirmPlateForWeekBeenPressedL = False
    app.hasConfirmPlateForWeekBeenPressedD = False
    app.tempPlates = dict()
    app.tempServingNums = dict()
    app.viewPlateReturnScreen = 'weeklySchedule'
    app.exerciseTypes = ['weightlifting', 'running', 'swimming']
    app.exerciseButtons = [
        Button(600, 210, 600, 70, 'weightlifting', 'lightGray', 'black', 14, 'center'),
        Button(600, 315, 600, 70, 'running', 'lightGray', 'black', 14, 'center'),
        Button(600, 420, 600, 70, 'swimming', 'lightGray', 'black', 14, 'center')
    ]
    app.selectedExerciseType = None
    app.exerciseDuration = 30
    app.exerciseToggleButtons = [
        Button(450, 525, 120, 70, '+', 'lightGray', 'black', 20, 'center'),
        Button(750, 525, 120, 70, '-', 'lightGray', 'black', 20, 'center')
    ]
    app.isExerciseConfirmed = {'Mon': False, 'Tues': False, 'Wed': False, 'Thurs': False, 'Fri': False, 'Sat': False, 'Sun': False}
    app.exerciseRoutineAddButton = Button(600, 612.5, 480, 61.25, 'Add Exercise', 'red', 'black', 14, 'center')
    app.exerciseRoutineViewButton = Button(1050, 420, 180, 40, 'View Routine', 'wheat', 'black', 14, 'center')
    app.exerciseRoutineConfirmButton = Button(1050, 460, 180, 40, 'Confirm Routine', 'lightGreen', 'black', 14, 'center')
    app.exerciseRoutineBackButton = Button(120, 70, 180, 52.5, 'Back', 'wheat', 'black', 12, 'center')
    app.hasSetRoutineForWeekBeenPressed = False
    app.setRoutineForWeekButton = Button(120, 140, 180, 60, 'Set routine for entire week?',
                                         'orange', 'black', 12, 'center')
    app.tempExerciseSession = None
    app.viewExerciseFromRoutineButton = Button(120, 595, 180, 52.5, 'View Routine', 'wheat', 'black', 14, 'center')
    app.viewPlateBackButton = Button(120, 70, 180, 52.5, 'Back', 'wheat', 'black', 14, 'center')
    app.viewRoutineBackButton = Button(120, 70, 180, 52.5, 'Back', 'wheat', 'black', 14, 'center')
    app.viewRoutineReturnScreen = 'weeklySchedule'
    app.simButtons = [
        Button(600, 250, 300, 70, '3 months', 'lightGray', 'black', 20, 'center'),
        Button(600, 350, 300, 70, '6 months', 'lightGray', 'black', 20, 'center'),
        Button(600, 450, 300, 70, '12 months', 'lightGray', 'black', 20, 'center')
    ]
    app.simPhase = 0
    app.simSteps = 0
    app.simString = ''
    app.simDone = False
    app.simResult = None
    app.stepsPerSecond = 30
    app.steps = 0
    
# Simulation

def simulation_onStep(app):
    if app.simPhase == 1:
        app.simSteps += 1
        if app.simSteps < 30:
            app.simString = 'Taking in data...'
        elif app.simSteps < 60:
            app.simString = 'Calculating results...'
        elif app.simSteps < 90:
            app.simString = 'Finalizing...'
        else:
            app.simPhase = 2
            app.simString = 'Completed!'
            app.simDone = True
            
def simulation_onMousePress(app, mouseX, mouseY):
    if app.simPhase == 0:
        for button in app.simButtons:
            if button.isClicked(mouseX, mouseY):
                if button.label == '3 months': horizon = 3
                elif button.label == '6 months': horizon = 6
                else: horizon = 12
                sim = SimulationConfig(horizon, app.weekPlan, app.avatars[app.selectedAvatarIndex])
                app.simResult = SimulationResult(sim, app.avatars[app.selectedAvatarIndex])
                app.simPhase = 1
                app.simString = 'Starting...'
    if app.simPhase == 2:
        app.showBodyImageChange = True
        setActiveScreen('avatar')
        
def drawSimulationScreen(app):
    drawLabel('Weekly Simulation', 600, 100, size = 30)
    if app.simPhase == 0:
        for button in app.simButtons:
            button.draw(app)
    elif app.simPhase == 1:
        drawLabel(app.simString, 600, 350, size = 28)
    elif app.simPhase == 2:
        result = app.simResult
        drawLabel('Simulation Complete!', 600, 200, size = 30, fill = 'green')
        drawLabel(f'Weight Change: {result.getWeightChange()} lbs', 600, 300, size = 22)
        drawLabel(f'BMI Change: {result.getBmiChange()}', 600, 350, size = 22)
        drawLabel('Want to run a simulation with another avatar? Click anywhere!', 600, 500, size = 18)
        
def simulation_redrawAll(app):
    drawSimulationScreen(app)
 
# Menu

def menu_onMousePress(app, mouseX, mouseY):
     for button in app.menuButtons:
            if button.isClicked(mouseX, mouseY):
                if button.label == 'Play': setActiveScreen('avatar')
                elif button.label == 'Instructions': setActiveScreen('instructions')
                
def menu_onMouseMove(app, mouseX, mouseY):
    for button in app.menuButtons:
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'yellow'
        else:
            button.backgroundColor = 'lightBlue'
            
 
def menu_redrawAll(app):
     drawMenuScreen(app)
     
# Instructions
     
def instructions_onMousePress(app, mouseX, mouseY):
    for button in app.instructionsButtons:
            if button.isClicked(mouseX, mouseY):
                if button.label == 'Back to Main': setActiveScreen('menu')
                
def instructions_onMouseMove(app, mouseX, mouseY):
    for button in app.instructionsButtons:
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'yellow'
        else:
            button.backgroundColor = 'wheat'
                
def instructions_redrawAll(app):
    drawInstructionsScreen(app)


# addName

def addName_redrawAll(app):
    drawLabel('Please type the name for this avatar!', 600, 95, size = 30, font = 'montserrat')
    drawLabel("Press 'enter' on your keyboard when done!", 600, 145, size = 20, font = 'montserrat')
    drawLabel(app.tempName, 600, 200, size = 25, font = 'montserrat')
    
    

def addName_onKeyPress(app, key):
    if key == 'enter':
        app.avatars.append(Avatar(app.tempName))
        app.namesList.append(app.tempName)
        app.selectedAvatarIndex = len(app.avatars) - 1
        app.tempName = ''
        app.imageNums[len(app.avatars)-1] = 2
        buildAvatarArchiveGrid(app)
        setActiveScreen('avatar')
    if key == 'space':
        app.tempName += ' '
    if key == 'backspace':
        app.tempName = app.tempName[:-1]
    if app.isTypingName and key != 'space' and key != 'enter' and key != 'backspace':
        if app.isShfitHeld:
            app.tempName += key.upper()
        else:
            app.tempName += key
        
def addName_onKeyHold(app, keys):
    if 'shift' in keys:
        app.isShiftHeld = True

def addName_onKeyRelease(app, key):
    if key == 'shift':
        app.isShiftedHeld = False

# Avatar
    
def avatar_onMousePress(app, mouseX, mouseY):
    for button in app.avatarButtons:
            if button.isClicked(mouseX, mouseY):
                if button.label == 'Add                                          ':
                    app.canCustomizeCharacter = True
                    if len(app.avatars) < 9:
                        app.isTypingName = True
                        setActiveScreen('addName')
                        return
                if app.canCustomizeCharacter:
                    avatar = app.avatars[app.selectedAvatarIndex]
                    if button.label == 'M': avatar.sex = 'male'
                    elif button.label == 'F': avatar.sex = 'female'
                    elif button.label == '+' and button.y == 260: avatar.age = (avatar.age or 0) + 1
                    elif button.label == '+' and button.y == 340: avatar.age = (avatar.age or 0) + 10
                    elif button.label == '+' and button.y == 430: avatar.height = (avatar.height or 0) + 1
                    elif button.label == '+' and button.y == 515: avatar.height = (avatar.height or 0) + 5
                    elif button.label == '+' and button.y == 605: avatar.weight = (avatar.weight or 0) + 1
                    elif button.label == '+' and button.y == 665: avatar.weight = (avatar.weight or 0) + 10
                    elif button.label == '-' and button.y == 260: avatar.age = max(0, (avatar.age or 0) - 1)
                    elif button.label == '-' and button.y == 340: avatar.age = max(0, (avatar.age or 0) - 10)
                    elif button.label == '-' and button.y == 430: avatar.height = max(0, (avatar.height or 0) - 1)
                    elif button.label == '-' and button.y == 515: avatar.height = max(0, (avatar.height or 0) - 5)
                    elif button.label == '-' and button.y == 605: avatar.weight = max(0, (avatar.weight or 0) - 1)
                    elif button.label == '-' and button.y == 665: avatar.weight = max(0, (avatar.weight or 0) - 10)
                    elif button.label == 'Confirm':
                        if (avatar.age is not None and avatar.height is not None
                            and avatar.weight is not None and avatar.sex is not None):
                            app.canConfirmCharacter = True
                            app.avatarButtons[0].backgroundColor = 'lightGreen'
                    avatar.updateBmi()
                if button.label == 'Look in archive':
                    app.imageNums[app.selectedAvatarIndex] = 2
                    setActiveScreen('avatarArchive')
                if app.canConfirmCharacter and button.label == 'Next step: Plan your weekly schedule':
                    setActiveScreen('weeklySchedule')

def avatar_onMouseMove(app, mouseX, mouseY):
    for button in app.avatarButtons:
        if button.label == 'Next step: Plan your weekly schedule': continue
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'yellow'
        else:
            if (button.label == 'Look in archive' or 
                button.label == 'Add' or button.label == 'Confirm'):
                button.backgroundColor = 'wheat'
            elif button.label == 'M': button.backgroundColor = 'lightBlue'
            elif button.label == 'F': button.backgroundColor = 'pink'
            else: button.backgroundColor = 'lightGray'
            
def avatar_onStep(app):
    if app.showBodyImageChange:
        app.steps += 1
        if app.simResult.getWeightChange() > 0:
            if app.steps == 30:
                app.imageNums[app.selectedAvatarIndex] += 1
                if app.simResult.getWeightChange() < 10:
                    app.steps = 0
                    app.showBodyImageChange = False
                    return
            elif app.steps == 60:
                app.imageNums[app.selectedAvatarIndex] += 1
                app.steps = 0
                app.showBodyImageChange = False
        elif app.simResult.getWeightChange() < 0:
            if app.steps == 30:
                app.imageNums[app.selectedAvatarIndex] -= 1
                if app.simResult.getWeightChange() > -5:
                    app.steps = 0
                    app.showBodyImageChange = False
                    return
            elif app.steps == 60:
                app.imageNums[app.selectedAvatarIndex] -= 1
                app.steps = 0
                app.showBodyImageChange = False
                
def avatar_redrawAll(app):
    drawAvatarScreen(app)
    
# Avatar Archive
    
def avatarArchive_onMousePress(app, mouseX, mouseY):
    for cell in app.avatarCells:
        if cell.x < mouseX < cell.x + cell.w and cell.y < mouseY < cell.y + cell.h:
            app.selectedAvatarIndex = cell.index
            app.canConfirmCharacter = False
            app.avatarButtons[0].backgroundColor = 'salmon'
    for button in app.avatarArchiveButtons:
        if button.isClicked(mouseX, mouseY):
            setActiveScreen('avatar')
                
def avatarArchive_redrawAll(app):
    drawAvatarArchiveScreen(app)
    
def avatarArchive_onMouseMove(app, mouseX, mouseY):
    for cell in app.avatarCells:
        if cell.x < mouseX < cell.x + cell.w and cell.y < mouseY < cell.y + cell.h:
            cell.hover = True
        else:
            cell.hover = False
    for button in app.avatarArchiveButtons:
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'yellow'
        else:
            button.backgroundColor = 'wheat'
            
# Weekly Schedule

def weeklySchedule_onMousePress(app, mouseX, mouseY):
    for i, (x, y, w, h) in enumerate(app.dayCells):
        if x < mouseX < x + w and y < mouseY < y + h:
            app.selectedDay = app.days[i]
    for component in app.weeklyScheduleButtons:
        button = app.weeklyScheduleButtons[component]
        if button.isClicked(mouseX, mouseY):
            if component == 'exercise':
                sessions = app.weekPlan.getExercises(app.selectedDay)
                if button.label == 'View Confirmed Routine':
                    setActiveScreen('viewRoutine')
                else:
                    setActiveScreen('exerciseRoutine')
            elif component in ['breakfast', 'lunch', 'dinner']:
                viewBtn = app.weeklyScheduleButtons[f'appViewPlate_{component}']
                confirmBtn = app.weeklyScheduleButtons[f'appConfirmPlate_{component}']
                confirmedPlate = app.weekPlan.getMealPlate(app.selectedDay, component)
                if app.weeklyScheduleButtons[component].label == 'View Confirmed Plate':
                    app.selectedMealType = component
                    app.viewPlateReturnScreen = 'weeklySchedule'
                    setActiveScreen('viewPlate')
                elif confirmedPlate is None:
                    key = (app.selectedDay, component)
                    app.selectedMealType = component
                    if key not in app.tempPlates:
                        app.tempPlates[key] = Plate()
                        app.tempServingNums[key] = 1
                    app.viewPlateReturnScreen = 'weeklySchedule'
                    setActiveScreen('category')
            elif component.startswith('appViewPlate_'):
                app.selectedMealType = component.split('_')[1]
                app.viewPlateReturnScreen = 'weeklySchedule'
                setActiveScreen('viewPlate')
            elif component.startswith('appConfirmPlate_'):
                mealType = component.split('_')[1]
                key = (app.selectedDay, mealType)
                if key in app.tempPlates and len(app.tempPlates[key].plate) > 0:
                    app.weekPlan.setMealPlate(app.selectedDay, app.tempPlates[key], mealType)
                if key in app.tempPlates:
                    del app.tempPlates[key]
                if key in app.tempServingNums:
                    del app.tempServingNums[key]
                app.selectedMealType = mealType
                setActiveScreen('weeklySchedule')
            elif component == 'confirm' and app.weekPlan.allDaysComplete():
                setActiveScreen('simulation')
    if app.showOrHideDailyInfoButton.isClicked(mouseX, mouseY):
        if app.showOrHideDailyInfoButton.label == 'Hide Daily Info':
            app.showDailyInfo = not app.showDailyInfo
            app.showOrHideDailyInfoButton.label = 'Show Daily Info'
        else:
            app.showOrHideDailyInfoButton.label = 'Hide Daily Info'
            app.showDailyInfo = not app.showDailyInfo
    if app.exerciseRoutineViewButton.isClicked(mouseX, mouseY):
        app.viewRoutineReturnScreen = 'weeklySchedule'
        setActiveScreen('viewRoutine')
    if app.exerciseRoutineConfirmButton.isClicked(mouseX, mouseY):
        app.isExerciseConfirmed[app.selectedDay] = not app.isExerciseConfirmed[app.selectedDay]

def weeklySchedule_redrawAll(app):
    drawWeeklyScheduleScreen(app)
    
def weeklySchedule_onMouseMove(app, mouseX, mouseY):
    for key, button in app.weeklyScheduleButtons.items():
        if key in ['breakfast', 'lunch', 'dinner', 'exercise', 'confirm']:
            if button.doesHover(mouseX, mouseY):
                button.backgroundColor = 'yellow'
            else:
                button.backgroundColor = 'lightGray'
    app.dayHoverIndex = None
    for i, (x, y, w, h) in enumerate(app.dayCells):
        if (x < mouseX < x + w and y < mouseY < y + h and app.days[i] != app.selectedDay and not 
            app.weekPlan.isDayComplete(app.days[i])):
            app.dayHoverIndex = i
            
# Category

def category_redrawAll(app):
    drawCategoryScreen(app)
    
def category_onMousePress(app, mouseX, mouseY):
    for button in app.categoryButtons:
        if button.isClicked(mouseX, mouseY):
            if button.label == 'Back':
                setActiveScreen('weeklySchedule')
            elif button.label == 'View Plate':
                app.viewPlateReturnScreen = 'category'
                setActiveScreen('viewPlate')
            else:
                app.selectedCategory = button.label
                app.foodCells = []
                app.foodItemSelected = None
                buildFoodCellGrid(app, app.selectedCategory)
                setActiveScreen('plateBuilder')
    
def category_onMouseMove(app, mouseX, mouseY):
    for button in app.categoryButtons:
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'lightYellow'
        else:
            button.backgroundColor = 'lightGray'
            
# Plate Builder

def plateBuilder_redrawAll(app):
    drawPlateBuilderScreen(app)
        
def plateBuilder_onMousePress(app, mouseX, mouseY):
    for cell in app.foodCells:
        if cell.foodCellisClicked(mouseX, mouseY) and cell.foodItem == app.foodItemSelected:
            app.isServingToggleButtonDrawn = False
        elif cell.foodCellisClicked(mouseX, mouseY):
            app.foodItemSelected = cell.getFoodItem()
            app.isServingToggleButtonDrawn = True
    for button in app.plateBuilderButtons:
        if button.isClicked(mouseX, mouseY):
            if button.label == '+':
                key = (app.selectedDay, app.selectedMealType)
                app.tempServingNums[key] += 1
            elif button.label == '-':
                key = (app.selectedDay, app.selectedMealType)
                app.tempServingNums[key] -= 1
                if app.tempServingNums[key] < 1:
                    app.tempServingNums[key] = 1
            elif button.label == 'Add to plate' and app.foodItemSelected != None:
                key = (app.selectedDay, app.selectedMealType)
                plate = app.tempPlates[key]
                plate.addFoodItem(app.foodItemSelected, app.tempServingNums[key])
                app.tempServingNums[key] = 1
                app.foodItemSelected = None
                app.isServingToggleButtonDrawn = False
            elif button.label == 'Remove from plate' and app.foodItemSelected != None:
                key = (app.selectedDay, app.selectedMealType)
                plate = app.tempPlates[key]
                plate.removeFoodItem(app.foodItemSelected, app.tempServingNums[key])
                app.tempServingNums[key] = 1
                app.foodItemSelected = None
                app.isServingToggleButtonDrawn = False
            elif button.label == 'View Plate':
                setActiveScreen('viewPlate')
            elif button.label == 'Back':
                setActiveScreen('category')
    if app.backPlateButton.isClicked(mouseX, mouseY): setActiveScreen('category')
    if app.viewPlateFromBuilderButton.isClicked(mouseX, mouseY):
        app.viewPlateReturnScreen = 'plateBuilder'
        setActiveScreen('viewPlate')
        
def plateBuilder_onMouseMove(app, mouseX, mouseY):
    for button in app.plateBuilderButtons:
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'yellow'
        else:
            button.backgroundColor = 'lightGray'
    for cell in app.foodCells:
        if cell.foodCellDoesHover(mouseX, mouseY):
            cell.backgroundColor = 'yellow'
        else:
            cell.backgroundColor = 'lightGray'
    if app.backPlateButton.doesHover(mouseX, mouseY): 
        app.backPlateButton.backgroundColor = 'yellow'
    else:
        app.backPlateButton.backgroundColor = 'wheat'
        
# Exercise
    
def exerciseRoutine_redrawAll(app):
   drawExerciseRoutineScreen(app)
    
def exerciseRoutine_onMouseMove(app, mouseX, mouseY):
    for button in app.exerciseButtons:
        button.backgroundColor = 'lightGray'
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'lightYellow'
    for button in app.exerciseToggleButtons:
        button.backgroundColor = 'lightGray'
        if button.doesHover(mouseX, mouseY):
            button.backgroundColor = 'yellow'
    if app.exerciseRoutineAddButton.doesHover(mouseX, mouseY):
        app.exerciseRoutineAddButton.backgroundColor = 'orange'
    else:
        app.exerciseRoutineAddButton.backgroundColor = 'red'
    if app.exerciseRoutineBackButton.doesHover(mouseX, mouseY):
        app.exerciseRoutineBackButton.backgroundColor = 'yellow'
    else:
        app.exerciseRoutineBackButton.backgroundColor = 'wheat'
        
def exerciseRoutine_onMousePress(app, mouseX, mouseY):
    for button in app.exerciseButtons:
        if button.isClicked(mouseX, mouseY):
            app.selectedExerciseType = button.label
    if app.selectedExerciseType is not None:
        plusButton, minusButton = app.exerciseToggleButtons
        if plusButton.isClicked(mouseX, mouseY): app.exerciseDuration += 5
        if minusButton.isClicked(mouseX, mouseY): app.exerciseDuration = max(5, app.exerciseDuration - 5)
        if app.exerciseRoutineAddButton.isClicked(mouseX, mouseY):
            newSession = ExerciseSession(
                app.selectedExerciseType,
                app.exerciseDuration,
                app.avatars[app.selectedAvatarIndex]
            )
            app.weekPlan.addExercise(app.selectedDay, newSession)
    if app.exerciseRoutineConfirmButton.isClicked(mouseX, mouseY):
        app.isExerciseConfirmed[app.selectedDay] = True
        setActiveScreen('weeklySchedule')
    if app.exerciseRoutineBackButton.isClicked(mouseX, mouseY):
        setActiveScreen('weeklySchedule')
    if app.viewExerciseFromRoutineButton.isClicked(mouseX, mouseY):
        app.viewRoutineReturnScreen = 'exerciseRoutine'
        setActiveScreen('viewRoutine')
        
# View Plate

def viewPlate_redrawAll(app):
    drawLabel(f'{app.selectedDay} - {app.selectedMealType.capitalize()} Plate', 600, 60, size = 28, font = 'montserrat')
    key = (app.selectedDay, app.selectedMealType)
    if key in app.tempPlates:
        plate = app.tempPlates[key]
    else:
        plate = app.weekPlan.getMealPlate(app.selectedDay, app.selectedMealType)
    if plate is None or plate.plate == dict():
        drawLabel('Your plate has nothing in it!', 600, 200, size = 20, fill = 'red', font = 'montserrat')
        app.viewPlateBackButton.draw(app)
    else:
        y = 150
        for foodItem, servings in plate.plate.items():
            drawLabel(f'{foodItem.foodName} | {servings} servings | {foodItem.kcalPerServ * servings} kcal',
                      600, y, size = 18, font = 'montserrat')
            y += 40
        drawLabel(f'Total: {plate.totalkCal} kCals', 600, y + 20, size = 22, fill = 'blue', font = 'montserrat')
        app.viewPlateBackButton.draw(app)
    if app.weekPlan.getMealPlate(app.selectedDay, app.selectedMealType) != None:
        if not hasConfirmedPlateForWeek(app, app.selectedMealType):
            app.setPlateForWeekButton.draw(app)
        
def viewPlate_onMousePress(app, mouseX, mouseY):
    if app.viewPlateBackButton.isClicked(mouseX, mouseY):
        setActiveScreen(app.viewPlateReturnScreen)
    if app.setPlateForWeekButton.isClicked(mouseX, mouseY):
        plate = app.weekPlan.getMealPlate(app.selectedDay, app.selectedMealType)
        app.weekPlan.setSamePlateForWeek(app, plate, app.selectedMealType)
        if app.selectedMealType == 'breakfast': app.hasConfirmPlateForWeekBeenPressedB = True
        elif app.selectedMealType == 'lunch': app.hasConfirmPlateForWeekBeenPressedL = True
        elif app.selectedMealType == 'dinner': app.hasConfirmPlateForWeekBeenPressedD = True
        
# View Exercise Routine Screen

def viewRoutine_redrawAll(app):
    drawLabel(f'{app.selectedDay} - Exercise Routine', 600, 60, size = 28, font = 'montserrat')
    sessions = app.weekPlan.getExercises(app.selectedDay)
    if len(sessions) == 0:
        drawLabel('No exercises added!', 600, 200, size = 20, fill = 'red', font = 'montserrat')
    else:
        totalBurn = 0
        y = 150
        for session in sessions:
            burned = session.caloriesBurnt()
            totalBurn += burned
            drawLabel(f'{session.typeOf} | {session.duration} min | {int(burned)} kcal burned', 600,  y, size = 18, font = 'montserrat')
            y += 40
        drawLabel(f'Total Burned: {int(totalBurn)} calories', 600, y + 20, size = 22, fill = 'blue', font = 'montserrat')
    app.viewRoutineBackButton.draw(app)
    if app.isExerciseConfirmed[app.selectedDay] and not app.hasSetRoutineForWeekBeenPressed:
        app.setRoutineForWeekButton.draw(app)
        
def viewRoutine_onMousePress(app, mouseX, mouseY):
    if app.viewRoutineBackButton.isClicked(mouseX, mouseY):
        setActiveScreen(app.viewRoutineReturnScreen)
    if app.viewExerciseFromRoutineButton.isClicked(mouseX, mouseY):
        app.viewRoutineReturnScreen = 'exerciseRoutine'
        setActiveScreen(app.viewRoutineReturnScreen)
    if app.isExerciseConfirmed[app.selectedDay] and app.setRoutineForWeekButton.isClicked(mouseX, mouseY):
        exercises = app.weekPlan.getExercises(app.selectedDay)
        app.weekPlan.setSameRoutineForWeek(app, exercises)
        app.hasSetRoutineForWeekBeenPressed = True
        
        
def main():
    runAppWithScreens(initialScreen = 'menu', width = 1200, height = 700)

main()
