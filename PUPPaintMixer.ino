const int MS1 = 52;
const int MS2 = 50;

const int R1 = 22;
const int R2 = 24;
const int R3 = 26;
const int R4 = 28;
const int R5 = 30;
const int R6 = 32;
const int R7 = 34;
const int R8 = 36;
String string = "50.0025.0025.0000.0000.00";

#include <NewPing.h>2 // don't forget to include the NewPing library.
NewPing Sonar1(33, 23, 400); 
NewPing Sonar2(33, 25, 400); 
NewPing Sonar3(33, 27, 400); 
NewPing Sonar4(33, 29, 400);  
NewPing Sonar5(33, 31, 400); 

float duration1;
float d1;
float duration2;
float d2;
float duration3;
float d3;
float duration4;
float d4;
float duration5;
float d5;

float P1;
float P2;
float P3;
float P4;
float P5;

float height1 = 17;
float height2 = 17;
float height3 = 17;
float height4 = 17;
float height5 = 17;

float SRead = 2.5;

float Speed1 = 7; //mL per second
float Speed2 = 7; //mL per second
float Speed3 = 7; //mL per second
float Speed4 = 7; //mL per second
float Speed5 = 7; //mL per second
//
//float Red;
//float Blue;
//float Yellow;
//float Black;
//float White;

int toDispense = 0;
String receivedChar;
int CleaningTime = 30;

float Red; char RedByte[10];
float Blue; char BlueByte[10];
float Yellow; char YellowByte[10];
float Black; char BlackByte[10];
float White; char WhiteByte[10];

char byteBuffer;
int index;
char *n;

void setup() {
    Serial.begin(9600);
    pinMode(MS1, INPUT);
    pinMode(MS2, INPUT);
    digitalWrite(MS1, HIGH);
    digitalWrite(MS2, HIGH);
    
    pinMode(R1, OUTPUT); digitalWrite(R1, HIGH);
    pinMode(R2, OUTPUT); digitalWrite(R2, HIGH);
    pinMode(R3, OUTPUT); digitalWrite(R3, HIGH);
    pinMode(R4, OUTPUT); digitalWrite(R4, HIGH);
    pinMode(R5, OUTPUT); digitalWrite(R5, HIGH);
    pinMode(R6, OUTPUT); digitalWrite(R6, HIGH);
    pinMode(R7, OUTPUT); digitalWrite(R7, HIGH);
    pinMode(R8, OUTPUT); digitalWrite(R8, HIGH);
//    CompoDown();
    CompoUp();
    receivedChar = Serial.readString();
    while (receivedChar != "1") {receivedChar=Serial.readString(); delay(100);}
    Serial.print("0");

    d1 = GetSonar1(); d2 = GetSonar2(); d3 = GetSonar3(); d4 = GetSonar4(); d5 = GetSonar5();

//    if (d1 > 10 || d2 > 10 || d3 > 10 || d4 > 10 || d5 > 10) {
//      Serial.print("0");
//      //while (1) {delay(1000);}
//      }
//    else {Serial.print("1");}
}

void loop() {
  receivedChar = Serial.readString();
       if (receivedChar == "A") {
        CompoDown(); 
        digitalWrite(R8, LOW); 
        GetDelays(); 
        toDispense = 1;
        Valve1(); Valve2();Valve3(); Valve4(); Valve5();
        digitalWrite(R8, HIGH);
        CompoUp();
        Serial.print("A");
        delay(50);
        }
  else if (receivedChar == "B") {GetPercentages(); delay(50);} 
  else if (receivedChar == "C") {
        CompoDown(); 
        digitalWrite(R8, LOW); 
        GetDelays(); 
        toDispense = 1;
//        Red = CleaningTime; Blue = CleaningTime; Yellow = CleaningTime; Black = CleaningTime; White = CleaningTime; 
//        Valve1(); Valve2();Valve3(); Valve4(); Valve5(); delay(50);
        digitalWrite(R1, LOW); digitalWrite(R2, LOW); digitalWrite(R3, LOW);
        digitalWrite(R4, LOW); digitalWrite(R5, LOW);
        
        for (int i = 0; i < CleaningTime; i++) {delay(1000);}
        digitalWrite(R1, HIGH); digitalWrite(R2, HIGH); digitalWrite(R3, HIGH);
        digitalWrite(R4, HIGH); digitalWrite(R5, HIGH);

        digitalWrite(R8, HIGH);
        CompoUp();
        Serial.print("A");
        delay(50);
    } 
  else if (receivedChar == "D") {
      Red = 1; Blue = 1; Yellow = 1; Black = 1; White = 1; 
      Valve1(); Valve2();Valve3(); Valve4(); Valve5();
  }
//  Serial.print(digitalRead(MS1));
//  Serial.println(digitalRead(MS2));
//  if (toDispense == 1) {Valve1(); Valve2();Valve3(); Valve4(); Valve5(); toDispense = 0;}
  //GetPercentages(); delay(1000);  
  else if (receivedChar == "E") {CompoUp(); delay(50);} 
  else if (receivedChar == "F") {CompoDown(); delay(50);} 
  else if (receivedChar == "G") {digitalWrite(R8, !digitalRead(R8)); delay(50);} 
  else if (receivedChar == "H") {
    CompoDown(); 
    digitalWrite(R8, LOW);
    for (int i = 0; i < 30; i++) {
      delay(1000);
      }
    digitalWrite(R8, HIGH);delay(50);
    CompoUp();
    Serial.print("A");
    }
 
//  
//  duration1 = Sonar1.ping(); d1 = duration1 / US_ROUNDTRIP_CM; delay(30);
//  duration2 = Sonar2.ping(); d2 = duration2 / US_ROUNDTRIP_CM; delay(30);
//  duration3 = Sonar3.ping(); d3 = duration3 / US_ROUNDTRIP_CM; delay(30);
//  duration4 = Sonar4.ping(); d4 = duration4 / US_ROUNDTRIP_CM; delay(30);
//  duration5 = Sonar5.ping(); d5 = duration5 / US_ROUNDTRIP_CM; delay(30);
//  Serial.print(digitalRead(MS1)); Serial.print(" "); 
//  Serial.print(digitalRead(MS2)); Serial.print(" "); 
//  Serial.print(d1); Serial.print(" "); 
//  Serial.print(d2); Serial.print(" "); 
//  Serial.print(d3); Serial.print(" "); 
//  Serial.print(d4); Serial.print(" "); 
//  Serial.print(d5); Serial.println(" "); 
}

void RelayGo(int RelayName, float Seconds) {
  digitalWrite(RelayName, LOW);
  int a = 0;
  for (int i = 0; i < Seconds; i++) {
    delay(1000);
    a++;
  }
  digitalWrite(RelayName, HIGH);
  }

void Valve1() {
//  digitalWrite(R1, LOW);
//  delay(Red*1000);
//  digitalWrite(R1, HIGH);
//  delay(1000);
  RelayGo(R4, Red);
  delay(1000);
  }

void Valve2() {
//  digitalWrite(R2, LOW);
//  delay(Blue*1000);
//  digitalWrite(R2, HIGH);
//  delay(1000);
  RelayGo(R2, Blue);
  delay(1000);
  }

void Valve3() {
//  digitalWrite(R3, LOW);
//  delay(Yellow*1000);
//  digitalWrite(R3, HIGH);
//  delay(1000);
  RelayGo(R3, Yellow);
  delay(1000);
  }

void Valve4() {
//  digitalWrite(R4, LOW);
//  delay(Black*1000);
//  digitalWrite(R4, HIGH);
//  delay(1000);
  RelayGo(R1, Black);
  delay(1000);
  }

void Valve5() {
//  digitalWrite(R5, LOW);
//  delay(White*1000);
//  digitalWrite(R5, HIGH);
//  delay(1000);
  RelayGo(R5, White);
  delay(1000);
  }

void CompoDown() {
  if (digitalRead(MS2) == 1) {
    digitalWrite(R7, LOW);
    delay(50);
    while (1) {if (digitalRead(MS2) == 0){break;}}
    digitalWrite(R7, HIGH);
    }
  }

void CompoUp() {
  if (digitalRead(MS1) == 1) {
    digitalWrite(R6, LOW);
    delay(50);
    while (1) {if (digitalRead(MS1) == 0){break;}}
    digitalWrite(R6, HIGH);
    }
  }

float GetSonar1() {
  duration1 = Sonar1.ping(); d1 = duration1 / US_ROUNDTRIP_CM; delay(30);
  return d1;
  }

float GetSonar2() {
  duration2 = Sonar2.ping(); d2 = duration2 / US_ROUNDTRIP_CM; delay(30);
  return d2;
  }

float GetSonar3() {
  duration3 = Sonar3.ping(); d3 = duration3 / US_ROUNDTRIP_CM; delay(30);
  return d3;
  }

float GetSonar4() {
  duration4 = Sonar4.ping(); d4 = duration4 / US_ROUNDTRIP_CM; delay(30);
  return d4;
  }

float GetSonar5() {
  duration5 = Sonar5.ping(); d5 = duration5 / US_ROUNDTRIP_CM; delay(30);
  return d5;
  }

void GetPercentages() {
  
  d1 = GetSonar1(); d2 = GetSonar2(); d3 = GetSonar3(); d4 = GetSonar4(); d5 = GetSonar5();
  P1 = -(100/(height1 - SRead))*(d1 - height1);
  P2 = -(100/(height2 - SRead))*(d2 - height2);
  P3 = -(100/(height3 - SRead))*(d3 - height3);
  P4 = -(100/(height4 - SRead))*(d4 - height4);
  P5 = -(100/(height5 - SRead))*(d5 - height5);
  Serial.print("AAA"); Serial.print(P1); Serial.print("BBB"); Serial.print(P2); Serial.print("CCC"); Serial.print(P3); Serial.print("DDD"); Serial.print(P4); Serial.print("EEE"); Serial.print(P5); Serial.print("FFF");
  }

void GetDelays1() {
  delay(250);
  while (!Serial.available()) {}
  string = Serial.readString();
  Red = string.substring(0,5).toFloat();  
  Blue = string.substring(5,10).toFloat();
  Yellow = string.substring(10,15).toFloat();
  Black = string.substring(15,20).toFloat();
  White = string.substring(20,25).toFloat();
  
  Red = ((float(Red)/100)*1000);
  Blue = ((float(Blue)/100)*1000);
  Yellow = ((float(Yellow)/100)*1000);
  Black = ((float(Black)/100)*1000);
  White = ((float(White)/100)*1000);
//
//  Serial.println(Red);
//  Serial.println(Blue);
//  Serial.println(Yellow);
//  Serial.println(Black);
//  Serial.println(White);

  Red = Red/Speed1;
  Blue = Blue/Speed2;
  Yellow = Yellow/Speed3;
  Black = Black/Speed4;
  White = White/Speed5;
//
//  Serial.println(Red);
//  Serial.println(Blue);
//  Serial.println(Yellow);
//  Serial.println(Black);
//  Serial.println(White);
  }

void GetDelays()
  {  
    Serial.flush();
    byteBuffer = 0;
    
    while(!Serial.available());
    char string[256];
    index = 0;
    
    do{
      if(Serial.available() > 0){
        byteBuffer = Serial.read();
        string[index] = byteBuffer;
        index++;
      }    
    }while(byteBuffer != 'Z'); 
  
    string[index] = '\0';
    n = strtok(string,",");
    n = strtok(NULL,",");strcpy(RedByte,n);
    n = strtok(NULL,",");strcpy(BlueByte,n);
    n = strtok(NULL,",");strcpy(YellowByte,n);
    n = strtok(NULL,",");strcpy(BlackByte,n);
    n = strtok(NULL,",");strcpy(WhiteByte,n);
  
    Red = atof(RedByte);
    Blue = atof(BlueByte);
    Yellow = atof(YellowByte);
    Black = atof(BlackByte);
    White = atof(WhiteByte);

    Red = ((float(Red)/100)*1000);
    Blue = ((float(Blue)/100)*1000);
    Yellow = ((float(Yellow)/100)*1000);
    Black = ((float(Black)/100)*1000);
    White = ((float(White)/100)*1000);

    Red = Red/Speed1;
    Blue = Blue/Speed2;
    Yellow = Yellow/Speed3;
    Black = Black/Speed4;
    White = White/Speed5;
  }
