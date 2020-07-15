from pySitrineoAna.dedx.dedxCalculator import dEdxCalculator 

calc = dEdxCalculator("../config/dEdx.cfg")
print(calc)
print(calc.GetCharge(10))
print(calc.GetdEdX(3))
print(calc.GetMomenta(3,11))


