const int pressureInput1 = A0; //select the analog input pin for the pressure transducer
const int pressureInput2 = A1;
const int pressureZero = 102.4; //analog reading of pressure transducer at 0psi
const int pressureMax = 921.6; //analog reading of pressure transducer at 100psi
const int pressuretransducermaxPSI = 10; //psi value of transducer being used
const int baudRate = 9600; //constant integer to set the baud rate for serial monitor
const int sensorreadDelay = 500; //constant integer to set the sensor read delay in milliseconds

float pressureValue1 = 0; //variable to store the value coming from the pressure transducer
float pressureValue2 = 0;
float s1 = 0;
float s2 = 0;
float offset1 = 0;
float offset2 = 0;


void setup() //setup routine, runs once when system turned on or reset
{
  Serial.begin(baudRate); //initializes serial communication at set baud rate bits per second
  
  // calibrates offset for 0 V during the first five seconds
  while (millis() < 5000) 
  {
    pressureValue1 = analogRead(pressureInput1); //reads value from input pin and assigns to variable
    pressureValue2 = analogRead(pressureInput2);
    pressureValue1 = ((pressuretransducermaxPSI)*(pressureValue1-pressureZero)/(pressureMax-pressureZero));
    pressureValue2 = ((pressuretransducermaxPSI)*(pressureValue2-pressureZero)/(pressureMax-pressureZero));

    //offsets for 0 PSI / 0 V
    offset1 = pressureValue1; 
    offset2 = pressureValue2;  
  }
}

void loop() //loop routine runs over and over again forever
{
  pressureValue1 = analogRead(pressureInput1); //reads value from input pin and assigns to variable
  pressureValue2 = analogRead(pressureInput2);
  pressureValue1 = ((pressuretransducermaxPSI)*(pressureValue1-pressureZero)/(pressureMax-pressureZero)); //converts voltage to a pressure value
  pressureValue2 = ((pressuretransducermaxPSI)*(pressureValue2-pressureZero)/(pressureMax-pressureZero));

  s1 = (pressureValue1 - offset1) * 51.7149; //converst PSI to mmHg
  s2 = (pressureValue2 - offset2) * 51.7149;

  char p1[8]; //initialize different pressures arrays
  char p2[4];
  dtostrf(s1, 4, 2, p1); //converts decimal to string
  dtostrf(s2, 4, 2, p2);

  //prints out pressure from sensor 1 and sensor 2 in the format of [00.00;00.00]
  Serial.print(p1);
  Serial.print(";");
  Serial.println(p2);
  
  delay(sensorreadDelay); //delay in milliseconds between read values
}