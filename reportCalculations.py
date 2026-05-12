import datetime as dt
from sql import GetHours, GetPayRate, GetDependents, GetDeductions
from decimal import Decimal

def CalculateGrossPay(empId, endDate):
    dbPayrate = GetPayRate(empId)[0]
    dbHours = GetHours(empId, endDate)

    payRate = Decimal(dbPayrate)

    grossPay = 0
    for i in dbHours:
        empId, date, hoursDb, ptoDb, lock = i
        day = dt.datetime.strptime(date, "%Y-%m-%d").strftime("%a")
        hours = Decimal(hoursDb)
        pto = Decimal(ptoDb)
        if day == 'Sun' or day == 'Sat':
            #gives all day overtime pay for weekend work
            grossPay += hours * payRate * Decimal("1.5")
        else:
            #gives straight pay for all hours worked
            grossPay += (hours + pto) * payRate
            if hours > Decimal("8"):
                #gives extra 50% for overtime hours
                grossPay += (hours - Decimal("8")) * Decimal("0.5") * payRate

    return grossPay

def CalculateNetPay(empId, grossPay):
    dbDependents = GetDependents(empId)[0]
    dependents = int(dbDependents)

     #find deductions for medical
    medical = 100 if dependents > 0 else 50

    #find employee stipend amount
    stipend = dependents * 45

    #find pay before taxes
    
    preTaxPay = Decimal(grossPay - medical + stipend)

    #get deductions from table
    deductionsText = GetDeductions()

    #build dictionary with deductions as percentages
    deductions = {}
    for tax, value in deductionsText:
        deductions[tax] = Decimal(value) * Decimal(".0001")

    #find value of each deduction
    for tax in deductions:
        deductions[tax] *= preTaxPay

    employeeDeductions = ['State Tax','Federal Tax Employee', 
                            'Social Security Tax Employee', 'Medicare Employee']
        
    #find net pay after tax
    netPay = preTaxPay
    for tax in employeeDeductions:
        netPay -= deductions[tax]

    #add pretax deductions/additions to dict
    deductions["Medical"] = medical
    deductions["Stipend"] = stipend

    return [netPay, deductions]
        