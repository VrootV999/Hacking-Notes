# Electrical & Hardware Hacking Basics

## Ohm’s Law


$ V = I / R $

Where:

* **V** = Voltage (Volts)
* **I** = Current (Amps)
* **R** = Resistance (Ohms)

**Rules:**

* Use **voltage across the component** for the calculation
* Use **series vs parallel rules** for correct voltage or current

---

## Power

$ P = V \times I = I^2 \times R = \frac{V^2}{R} $

* Power in watts measures energy used by components
* Useful for LEDs, resistors, regulators

---

## Series Circuit

* Components connected **one after another**
* **Current is constant** across all components
* **Voltage splits** across each component
* **Total resistance** = sum of resistances

Example:

```
VCC → R1 → R2 → R3 → GND
```

* I = same everywhere
* V1 = I × R1
* V2 = I × R2

--- 
## Inductors
They are just wires coiled up. They create a magnetic field and it is the strongest in the center.
- So the current when it passes throught the wire throught the inductors and the energy is stored in this magnetic 
field
- The capacity of Inductor is called as Inductance.
- The energy stored in Inductor is measured in Henry(L).(Named after Joseph Henry)
- If current increase, the inductor opposes it.
- If current decrease, the inductor tries to keep it flowing.
- In alternating current there is a bit of impedance created.
- The resistance created by inductors in alternating current by an inductor is called as Reactance(XL).

$ XL = 2\pi fL$

- Higher frequency = Higher reactance

---
## Capacitors
- They are the electronic components that stores electrical energy in an electric field.
- It is simply two electrical plates divided by an insulator(dielectric).
- Key properly of Capacitors is Capacitance and it is measured in farades(F).(Named after Michael Faraday)
- It represents how much charge the Capacitors can store per volt.

$ Q = C \times V $

### Working Principle of a Capacitors
Charging
- Electrons accumulate on one plate.
- The opposite plate loses electrons.
- An electric field forms between the plates.
- Energy is stored in that field.

Discharging
- When the circuit is closed through a load, the stored energy flows out as current.
- Energy stored in a capacitor:

### Behavior of Capacitors
#### In a DC Circuit

Initially
- Capacitor behaves like a short circuit.
- Current flows while the capacitor charges.

After fully charged
- Voltage across capacitor equals source voltage.
- Current becomes zero.
- Capacitor behaves like an open circuit.

Uses in DC circuits
- Energy storage (backup supply)
- Filtering ripple in power supplies
- Timing circuits (RC circuits)
- Coupling/decoupling in electronic circuits
- Memory and pulse circuits
$ E = \frac{1}{2} C V^2 $

#### In a AC Circuit
- Current isn't blocked in AC.
- Current flows and the Capacitors continuously charges and discharges
- Resistance increases as frequency decreases
$ X_C = \frac{1}{2 \pi f C} $

- Impeadace is the generalisation of resistance for a AC circuit.
- In other words, the opposition that circuit offers to the flow of alternating current.
- Impedance(Z) is calculated with the formula
$Z = \sqrt{R^2 + X^2}$
$ Z = R + jX$

- Higher Frequency = Lower Reactance

---
## Summary and Differentiate

| Feature                        | **Capacitor**                                             | **Inductor**                                        |
| ------------------------------ | --------------------------------------------------------- | --------------------------------------------------- |
| **Basic Idea**                 | Stores energy in an **electric field** between two plates | Stores energy in a **magnetic field** around a coil |
| **Main Structure**             | Two conductive plates separated by a **dielectric**       | **Coil of wire** often wound around a core          |
| **Unit**                       | **Farad (F)** named after Michael Faraday                 | **Henry (H)** named after Joseph Henry              |
| **What It Opposes**            | Opposes **change in voltage**                             | Opposes **change in current**                       |
| **Energy Storage**             | Electric field between plates                             | Magnetic field around coil                          |
| **Energy Formula**             | $ E=\frac{1}{2}CV^2 $                                      | $ E=\frac{1}{2}LI^2 $                           |
| **Voltage / Current Equation** | $ I = C\frac{dV}{dt} $                                     | $ V = L\frac{dI}{dt} $                               |
| **DC Behaviour**               | After charging → behaves like **open circuit**            | After steady state → behaves like **short circuit** |
| **AC Behaviour**               | Allows AC to pass depending on frequency                  | Opposes AC more as frequency increases              |
| **Impedance (AC)**             | $ X_C=\frac{1}{2\pi fC} $                                   | $ X_L=2\pi fL $                                      |
| **Effect of Frequency**        | Higher frequency → **lower reactance**                    | Higher frequency → **higher reactance**             |
| **Phase Relationship (AC)**    | Current **leads voltage by 90°**                          | Current **lags voltage by 90°**                     |
| **Resistance**                 | Ideally **0 resistance**, only reactance                  | Ideally **0 resistance**, only reactance            |
| **Energy Release**             | Releases stored electric energy when discharging          | Magnetic field collapses and releases energy        |
| **Typical Uses**               | Filters, coupling, energy storage, timing circuits        | Filters, transformers, motors, power supplies       |
---
## Diodes
Diodes does nothing when the polarity is correct and if it is inverted it blocks current
(except leakage current flows) hence blocking it completly.

characteristics of diode
- Forward bias voltage
    The current flows in a circuit with proper polarity of diode only when the voltage provided is GREATEST
    Than the forward bias voltage
    Standard Diodes: Vf = ~0.6V
- Reverse Breakdown voltage
    The voltage that when passed in a reverse setup of diode will allow current to flow through without any       
    impedance(Diode Breakdown).
    Standard Diodes: Vbr = -50V

In AC
- The diode works the same but AC becomes pulsating
- Add capacitors to make it simalar to DC(with diodes)
- It can be used to make a full-wave rectifier

---
## Transistors
- Used as an Electric Switch(Either open or close)
- Used as an Amplifier(a range of value open/close/kinda)

Two types of Transistors
BJT(Bipolar Junction Transistors): Three layer(emitter-base-collector); Either NPN/PNP.
- The difference between The base and emitter is Vbe.
- Voltage is provided through the base to manipulate the amount of current to flow through.
- The path of current flown between the base and the emitter can act as a diode.
- Vary the input voltage to do amplifying in the saturation region.
- Vbe fluctuating in the saturation region make it amplify.
- To fully open/close you'd go greater than the Vf(forward bias voltage).
- The voltage in emitter is Ve
- The voltage in collector is Vc
- The voltage in the base is Vb

- Cutoff : Switch is off so no flow
- Active : Amplifier
- Saturation: switch on
- In Ac they tend to increase the strength 


FET(Field Electric Transistors) Three Terminals(Gate-source-Drain); Either JFET(JunctionFET)/MOSFET(Metal-Oxide-SemiConductor)


---

## Parallel Circuit

* Components connected across **same two nodes**
* **Voltage is constant** across each branch
* **Current splits** among branches
* **Total resistance** = less than smallest resistor

Example:

```
      ┌── R1 ──┐
VCC ──┤       ├── GND
      └── R2 ──┘
```

* V1 = V2 = total voltage
* I1 = V / R1
* I2 = V / R2
* I_total = I1 + I2

---
## Amperes Law
Amperes law states that Magnetic field induces currents. Especially when there is change in direction.
- the wire is moved.
- AC is used.

---

## Kirchhoff’s Laws

### Kirchhoff’s Current Law (KCL)

At any node:

```
Current entering = Current leaving
```

* Useful for **branching circuits**
* Always identify the node first

---

### Kirchhoff’s Voltage Law (KVL)

Around any closed loop:

```
Sum of voltage rises = Sum of voltage drops
```

* Useful for **series loops**
* Helps calculate unknown voltages

---

## Voltage Dividers

Used to reduce voltage:


$ V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2} $

* Common on sensors and ADC inputs
* Can appear in tamper circuits, logic level shifting

---

## Pull-Up / Pull-Down Resistors

* Pull-up: keeps input **high** when switch is open
* Pull-down: keeps input **low** when switch is open

Example:

```
3.3V
 |
[10kΩ]
 |
 MCU PIN
 |
BUTTON → GND
```

* Button open → MCU reads **3.3V (HIGH)**
* Button pressed → MCU reads **0V (LOW)**
* Current through resistor = V / R = 0.33 mA

---

## LEDs & Current Limiting

* LEDs require a resistor to limit current
* Series with LED:
  $ I = \frac{V_{supply} - V_{LED}}{R} $
* Common resistor values depend on voltage and desired current

---

## Short Circuit & Safety

* Always calculate expected current before probing a board
* Ohm’s law for shorts:
  $ I = V / R $
* Prevents board damage and blown traces

---

## Steps to Analyze a Circuit (Hardware Hacker Approach)

1. Identify **power source (VCC, GND)**
2. Identify **series vs parallel paths**
3. Determine **what is constant**:

   * Series → current constant
   * Parallel → voltage constant
4. Apply **Ohm’s law** for components
5. Apply **KCL** at nodes, **KVL** in loops
6. Estimate current/voltage mentally
7. Verify using a multimeter or simulator

---

## Practical Hardware Hacking Tips

* Recognize **common circuit patterns**:

  1. Pull-up / pull-down inputs
  2. LED indicators with resistors
  3. Voltage dividers
  4. Linear regulators (V_drop → heat)
  5. Oscillator / crystal circuits
  6. MOSFET switches
  7. Capacitor decoupling

* Start with **simulation tools**:

  * Falstad Circuit Simulator
  * CircuitLab
  * LTspice

* Once confident, move to **multimeter & scope** on real boards

* Build **pattern recognition**:

---

## Electrical Lab Safety

- Be careful while working with circuits.
- any current above 10mA can cause issues like involuntary muscle contraction, difficulty in breathing
  ventricular fibrillation, etc..
- Power on circuits when required.
- Remove any jewelry.
- Be careful when messing with capacitors.
- Don't discharge into electronic components. take measures.

---

## Tools Required
- Phillip Screwdrivers
- Spudging tools(also picks and screwdrivers are good)(in case of pressure fitted parts)
- Multimeter
- UART connector
- Jumper Wires(mainly M-F,M-M,F-F) & Headers
- Soldering Iron
- Wire Strippers(just a scissor if you are cheap)
- Logic analyser(Saleae Logic Analyser/DSLogic)
- SPI/i2c/Flash Dumping tools (bus pirate, CH341A USB Programmer, SOIC8 clip)
- SEGGER J-Link Debug Probe
- ST-Link V2
- NAND Adapter
- TL866II Plus Universal Programmer()
- CH341A USB Programmer
- Pomona 5250 SOIC-8 Test Clip
- RT809H Universal Programmer
- Easy JTAG Plus
- JTAGULATOR
- SOIC8 clip
- Jlink
- Hooks
- exploiteers
- Hydra Bus
- Shikra
- GreatFET
- GlassLow interface Explorer
- FTDI232 chip
- FT232H Breakout Board

---

## Notes
- Take notes on the hardware,procedure,schematics,readings etc.. properly.

```md
Target: Name Model
Sno: xxxxx
Test Date: xx/xx/xxxx
Procedure: <put the steps>
```

---

## Current

- DC: Direct Current Which has fixed voltage.
- AC: Alternating Current Which has Fluctuating voltage(in sine wave)
      US/Ca/Mexico/Sk/Phillipines/Taiwan: 120VAC 60Hz 
      Ind/Uk/Ger: 230VAC 50Hz 
      Fr/Ch: 230VAC 50hz
- Hz says how many times current changes direction per second.

- In a sine wave there are 3 main parts
    - Amplitude: The total distance from mid level(0) to the Peak voltage.
    - Peak Voltage(Vp): Is the highest voltage thats represented.(also called as amplitude)(highest ever it has gone)
    - Peak to Peak Voltage(Vpp): The lowest the wave has gone.
    - In AC, the Voltage is Calculated through RMS(Root Mean Square)
    $ V_{p} = V_{RMS} \times \sqrt{2} $ 
    $ V_{RMS} = \frac{V_{p}}{\sqrt{2}} $  
    $ V_{RMS} = \frac{V_{pp}}{2\sqrt{2}} $
    $ V_{pp} = 2 \times V_{p} $
    $ V_{pp} = 2\sqrt{2} \times V_{RMS} $

- In a Square Wave there are main parts.
    - Pulse width: says how long does the pulse go on for.
    - Duty Cycle(D): Ratio of the PulseWidth according with
    $ PulseWidth = Period/Time $

---

## Basic Procedure of Work

- Verify the input voltage
- Check for UART conncetion.

---

## Electronic Communication and Signals
### Analog Signals
- They vary in voltage and frequency to represent something
- There is continuous voltage signal and no bit designation.
- Ex: Microphones and Speakers

### Digital Signals
- There is just two types of its extreem low and high or 0 and 1.
- Mostly represented in Square wave.
- To diferentiate each bit we'd use time as a basis which is called as Symbol duration.$T_s$
- Symbols per seconds is measured in 1/Ts and it is called as baud rate(mostly used)/bit rate

---
## UART(Universal Asynchronous Receiver Transmitter)
A piece of hardware that helps us to Asynchronous Communication
- Old but still used.
- No clock signal/shared clock
- We use baud rate as usual
Basically 4 pins
- Tx(Transmit pin): Transmits out voltages.
- Rx(Reciever pin): Find changes in Voltages.
- Ground pin: A common Ground is necessary b/w two devices.
- Vcc : to supply power(not necessary for hacking) but can be used to power other devices using Vcc.

Connection
- Tx to Rx(both ways, depending on need and if software and designer created protocol for it)
- (Optional on either recieving or listening)
- Gnd to Gnd

If not labeled
- Commonly might have small changes
- check for ground at the 4 holes you see(using continuity test)
- Check a port for Vcc using Voltmeter(A specific voltage can be seen coming through)
- 0V at the Rx pin always
- While booting there will be great changes in Tx pin and will go to either 0-1V or so.
- Normally Tx port have the same voltage as the Vcc port.

Use pulseview to view the transmitted packets

---
## OSINT and RECON

- nmap scan first
`sudo nmap -T4 -p- -A xxx.xxx.xxx.xxx`
`sudo nmap -sU --top-ports 200 xxx.xxx.xxx.xxx`
- boot procees and sheel in UART
`sudo screen /dev/usbdev bard-rate`
- visit the website hosted locally
- file transfer(boot image/tools)
`sudo atftpd --daemon`
send
`tftp -l <location> -p <ip>` best to send from cwd instead of full path
recieve
`tftp -r <file to recieve> -g <ip>`


---
## SPI protocol
SPI (Serial Peripheral Interface) is a protocol which is used to communicate synchronous
- They work in Master-Slave setup
- Master initiates all communication by providing the clock cycle.
- The communication is full-duplex
- Multiple slaves can be connected to one master.
- Slave can't connect to Slave
- The four main (minimum)signals are.
    - SCLK = clock: The clock signal
    - CS = Chip select: A enable button for SPI chip
    - MOSI = Master out Slave in: The chip recieves data from the master.
    - MISO = Master in Slave out: The slave provides data to the master.
- The slave is the Nor Flash chip
- The master is the microcontroler

---
## ROM types
- NOR flash:    comes in SOIC packages: SOIC8 (low density)
- NAND flash:   comes in TSOP packages: TSOP38 (high density)
- eMMC flash:   comes in BGA packages: BGA{153}(ball grid array) (highest density)
- UFS flash: new type

### NOR flash
- Storage medium for non-volatile data.
- data can be read and written byte per byte.
- "fault free" memory
- low latency
- mostly used for low-storage
- communicated via SPI(Serial Peripheral Interface)
- they come in SOIC package
- Check the datasheet always
- You'd only need to know where the power and ground to not mess the chip.

### NAND flash
- 
