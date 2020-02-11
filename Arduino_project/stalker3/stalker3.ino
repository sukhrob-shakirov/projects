int right = 2;
int mid = 1;
int left = 0;
int alpha = 9;
int beta = 8;
int rD, lD, mD, L,R,M, maxM,maxR,maxL;
int a=1,b=1;
unsigned long timeI,timeF,relaxTime=1000,offTime=500;
unsigned long time1,time2;

void start(){
  timeI=millis();
  digitalWrite(10,HIGH);
  delay(500); 
}
void motorON(){
  if(a==1){
    start();
  }
  digitalWrite(10,HIGH);
  b=1;
  a=0;
  timeF=millis();
  if(timeF-timeI>relaxTime){
    digitalWrite(10,LOW);
    delay(offTime);
    timeI=millis();
  }
}
void motorOFF(){
  if(b==1){
    time1=millis();
  }
  time2=millis();
  if(time2-time1>5000){
    lD = analogRead(left)+10;
    rD = analogRead(right)+10;
    Serial.println(time2-time1);
    time1=millis();
  }
  digitalWrite(10,LOW);
  a=1;
  b=0;
}

void leftM(){
  digitalWrite(alpha, HIGH);
  digitalWrite(beta,LOW);
}
void rightM(){
  digitalWrite(alpha, LOW);
  digitalWrite(beta, HIGH);
}
void straightM(){
  digitalWrite(alpha, LOW);
  digitalWrite(beta,LOW);
}

void setup() {
  pinMode(10,OUTPUT);
  pinMode(beta, OUTPUT);
  pinMode(alpha, OUTPUT);
  rD = analogRead(right)+20;
  lD = analogRead(left)+20;
  mD = analogRead(mid)+25;
  maxM = mD+80;
  maxR = rD+80;
  maxL = lD+80;
  Serial.begin(9600);
}
void loop() {
  R = analogRead(right)-rD;
  M = analogRead(mid)-mD;
  L = analogRead(left)-lD;
  Rx = analogRead(right);
  Mx = analogRead(mid);
  Lx = analogRead(left);

  if(M>0 && M>R && M>L && Mx<maxM){
    straightM();
    motorON();
  }else if(L>0 && L>M && L>R && Rx<maxR){
    leftM(); 
    motorON();
  }else if(R>0 && R>M && R>L && Lx<maxL){
    rightM();
    motorON();
  }else{
    straightM();
    motorOFF();
  }
    
}
