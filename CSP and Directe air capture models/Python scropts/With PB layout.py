import CoolProp.CoolProp as CP
import numpy as np

T1 = T2 = T3 = T5 = 0
rf = "Air"
T4 = 850
T2 = 1000
Qdac = 128

T2_pb = T3_pb = T5_pb = 0
Ta = 9
T1_pb = 180
rf = "Air"
pressure = 101325

W_pb = 13  # MW

effComp = 0.81
effTurb = 0.84
effMech = 0.98
effGen = 0.96
effInv = 0.96
beta = 4.1

# content of captured gas

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
Qpreheat = heatCapacity_pellet * (To - Ti) / 0.7 / 1000000  # = 55.6001 MW



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

    while 1 > 0:

        h4 = calc_h_gas(T4)
        h5 = calc_h_gas(T5)
        Q4_5 = (h4 - h5) * mass / 1000000
        if (Q4_5 - Qpreheat) > 0 and (Q4_5 - Qpreheat) < 0.1:
            return T5
        else:
            T5 -= deltaTemp

        if i == 3000:
            print("error in mass calculation, loop limit " + str(T5))
            break
        i += 1


def temp_calc_fromEnthalpy(enthalpy, temperature):
    i = 1
    Tx = temperature
    deltaTemp = 0.1
    # print(Tx)
    while 1 > 0:
        # print(Tx)
        hx = calc_h_gas(Tx)
        if abs(enthalpy - hx) < 1000:
            return Tx
        else:
            Tx -= deltaTemp

        if i == 5000:
            print("error in temperature calculation, loop limit " + str(Tx))
            break
        i += 1


# ------------------------ calculation -----------------------------


h_a = CP.PropsSI("H", "P", pressure, "T", Ta + 273, rf)
h_1_pb = CP.PropsSI("H", "P", pressure * beta, "T", T1_pb + 273, rf)

T2_pb = 0
j = 0

pitch = 18

i = 0
while 1 > 0:
    T3 = T2 - pitch
    print(T3)
    print("i =",i)

    massGasCirc = Qdac / (calc_h_gas(T3) - calc_h_gas(T4)) * 1000000
    massGas = massGasCirc + m_cap_N2 + m_cap_CO2 + m_cap_O2

    T5 = T5_calc(massGas)
    h_5 = calc_h_gas(T5)
    pitch2 = 5
    while 1 > 0:
        print("j= ",j)
        j += 1


        T3_pb = T5 - pitch2
        h_3_pb = CP.PropsSI("H", "P", pressure * beta, "T", T3_pb + 273, rf)
        s_3 = CP.PropsSI("S", "P", pressure * beta, "T", T3_pb + 273, rf)

        h_4is_pb = CP.PropsSI("H", "P", pressure, "S", s_3, rf)
        h_4_pb = h_3_pb - effTurb * (h_3_pb - h_4is_pb)
        T4_pb = CP.PropsSI("T", "P", pressure, "H", h_4_pb, rf) - 273
        m_pb = W_pb * 1000000 / (effGen * effInv * (effMech * (h_3_pb - h_4_pb) - (h_1_pb - h_a)))
        T2_pb = 0.86 * (T4_pb - T1_pb) + T1_pb
        h_2_pb = CP.PropsSI("H", "P", pressure * beta, "T", T2_pb + 273, rf)
        print("T2_pb=", str(T2_pb), "T3_pb=", str(T3_pb),"T4_pb=", str(T4_pb), "m_pb = ", m_pb, "m_circ = ",massGasCirc)

        h_6 = h_5 - (m_pb / massGasCirc) * (h_3_pb - h_2_pb)
        print("h_6=", str(h_6), "h_5=", str(h_5))
        T6 = temp_calc_fromEnthalpy(h_6, T5)

        if ((T5 - T6) / (T5 - T2_pb)) < 0.86 or abs((T5 - T6) / (T5 - T2_pb) - 0.86) < 0.05:
            print("T6=", str(T6), "hex_5_6 eff =", str((T5 - T6) / (T5 - T2_pb)))
            break
        if j > 5000:
            print("error pechal")
            break

        pitch2 += 0.5


    if abs(900 - T3 + 0.1 * T6) < 0.5 or (900 - T3 + 0.1 * T6) > 0:
        # print(T5)
        print("T3 =" + str(T3) + "  T6 =" + str(T6) + "  T5 =" + str(T5) + " pitch =" + str(pitch))
        break

    if i == 5000:
        print("error, loop max limit")
        break
    i += 1
    pitch += 0.5
    print("====================")
