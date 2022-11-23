import CoolProp.CoolProp as CP
import numpy as np

T1 = T2 = T3 = T5 = 0
rf = "Air"
T4 = 850
T2 = 1000
Qdac = 128


# content of gas

CO2_fraction = 0.9713
O2_fraction = 0.0136
N2_fraction = 0.0151

# captured

m_cap_CO2 = 46.09883
m_cap_O2 = 0.645469
m_cap_N2 = 0.716661

# pellet props. It should be preheated up to 650 C

Ti = 300
To = 850
eff = 0.7
m_Ca = 83.33
m_K2 = 1.5
cp_Ca = 834.3
cp_K2 = 827.7

heatCapacity_pellet = m_Ca * cp_Ca + m_K2 * cp_K2
Qpreheat = heatCapacity_pellet * (To - Ti)/0.7/1000000  # = 55.6001 MW

print(Qpreheat)

# ------------------------ functions -----------------------------


def calc_h_gas(temperature):
    h_CO2 = CO2_fraction * CP.PropsSI("H", "P", 1e5, "T", temperature + 273, "CO2")
    h_O2 = O2_fraction * CP.PropsSI("H", "P", 1e5, "T", temperature + 273, "O2")
    h_N2 = N2_fraction * CP.PropsSI("H", "P", 1e5, "T", temperature + 273, "N2")
    return h_N2 + h_O2 + h_CO2

def T5_calc(mass):
    i = 1

    T5 = T4 - 10
    deltaTemp = 0.1

    while 1>0:

        h4 = calc_h_gas(T4)
        h5 = calc_h_gas(T5)
        Q4_5 = (h4-h5)*mass/1000000
        if (Q4_5 - Qpreheat)>0 and (Q4_5 - Qpreheat) < 0.1:
            return T5
        else:
            T5 -= deltaTemp

        if i == 3000:
            print("error in mass calculation, loop limit " + str(T5))
            break
        i += 1


# ------------------------ calculation -----------------------------


pitch = 18


i = 0
while 1 > 0:
    T3 = T2 - pitch
    print(T3)
    massGasCirc = Qdac / (calc_h_gas(T3) - calc_h_gas(T4)) * 1000000
    massGas = massGasCirc + m_cap_N2 + m_cap_CO2 + m_cap_O2

    T5 = T5_calc(massGas)
    # print(T5)
    if abs(900 - T3 + 0.1*T5) < 0.5 or (900 - T3 + 0.1*T5) > 0:
        # print(T5)
        print("T3 =" + str(T3) + "  T5 =" + str(T5) + " pitch ="+ str(pitch))
        break

    if i == 5000:
        print("error, loop max limit")
        break
    i += 1
    pitch += 0.5





# T3 = 980
# # print(T3)
# massGasCirc = Qdac / (calc_h_gas(T3) - calc_h_gas(T4)) * 1000000
# massGas = massGasCirc + m_cap_N2 + m_cap_CO2 + m_cap_O2
# # print(massGas)
#
# T5 = T5_calc(massGas)
# print(T5)