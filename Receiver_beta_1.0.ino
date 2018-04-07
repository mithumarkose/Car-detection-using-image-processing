#include<SPI.h>
#include<RF24.h>
const uint64_t pipe = 0xE8E8F0F0E1LL ;
RF24 radio(9, 10);
void setup()
{
  while (!Serial);
  Serial.begin(9600);
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openReadingPipe(1, pipe);
  radio.enableDynamicPayloads();
  radio.powerUp();

}
void loop(void)
{
 // Serial.println("hi");
  radio.startListening();
  char recmsg[32] = {0};
  if (radio.available())
  {
    radio.read(recmsg, 1);
    char msg[32] = {0} ;
    if (radio.available()) {
      radio.read(msg, sizeof(msg));
      Serial.println(msg) ;
      radio.stopListening() ;
      delay(100);
    }
  }
}

