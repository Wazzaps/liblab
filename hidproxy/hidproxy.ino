#include <Keyboard.h>
#include <Mouse.h>

enum {
  MODE_TTY,
  MODE_RAW,
} g_mode = MODE_TTY;

enum raw_op {
  OP_NOP = 0,
  OP_IDENTIFY,
  OP_TTY_MODE,
  OP_KEYBOARD_PRESS,
  OP_KEYBOARD_RELEASE,
  OP_KEYBOARD_RELEASE_ALL,
  OP_KEYBOARD_TYPE,
  OP_MOUSE_PRESS,
  OP_MOUSE_RELEASE,
  OP_MOUSE_CLICK,
  OP_MOUSE_MOVE,
};

void setup() {
  Serial1.begin(115200);
  pinMode(13, OUTPUT);
  Keyboard.begin();
  Mouse.begin();
}

char getc() {
  while (Serial1.available() == 0);
  return Serial1.read();
}

void loop() {
  char c = getc();
  digitalWrite(13, 1);

  switch (g_mode) {
  case MODE_TTY:
    if (c == 0) {
      g_mode = MODE_RAW;
    } else if (c == '\r') {
      Keyboard.write(KEY_RETURN);
      Serial1.write('\r');
      Serial1.write('\n');
    } else if (c == 127) {
      Keyboard.write(KEY_BACKSPACE);
      Serial1.write('\b');
      Serial1.write(' ');
      Serial1.write('\b');
    } else if (c == 3) {
      Keyboard.press(KEY_LEFT_CTRL);
      delay(5);
      Keyboard.press('c');
      delay(5);
      Keyboard.releaseAll();
      Serial1.write('^');
      Serial1.write('C');
    } else if (c == 4) {
      Keyboard.press(KEY_LEFT_CTRL);
      delay(5);
      Keyboard.press('d');
      delay(5);
      Keyboard.releaseAll();
      Serial1.write('^');
      Serial1.write('D');
    } else if (c == 12) {
      Keyboard.press(KEY_LEFT_CTRL);
      delay(5);
      Keyboard.press('l');
      delay(5);
      Keyboard.releaseAll();
      Serial1.write('^');
      Serial1.write('L');
    } else {
      Keyboard.write(c);
      Serial1.write(c);
    }
    break;
  case MODE_RAW:
    switch (c) {
    case OP_IDENTIFY:
      Serial1.println("[HIDProxy 1.0]");
      for (size_t i = 0; i < 10; i++) {
        digitalWrite(13, 1);
        delay(100);
        digitalWrite(13, 0);
        delay(100);
      }
      break;

    case OP_TTY_MODE:
      g_mode = MODE_TTY;
      break;
    case OP_KEYBOARD_PRESS: {
      char code = getc();
      Keyboard.press(code);
      break;
    }
    case OP_KEYBOARD_RELEASE: {
      char code = getc();
      Keyboard.release(code);
      break;
    }
    case OP_KEYBOARD_RELEASE_ALL:
      Keyboard.releaseAll();
      break;
    case OP_KEYBOARD_TYPE: {
      char code = getc();
      Keyboard.write(code);
      break;
    }
    case OP_MOUSE_PRESS: {
      char code = getc();
      Mouse.press(code);
      break;
    }
    case OP_MOUSE_RELEASE: {
      char code = getc();
      Mouse.release(code);
      break;
    }
    case OP_MOUSE_CLICK: {
      char code = getc();
      Mouse.click(code);
      break;
    }
    case OP_MOUSE_MOVE: {
      signed char dx = (signed char) getc();
      signed char dy = (signed char) getc();
      signed char dw = (signed char) getc();
      Mouse.move(dx, dy, dw);
      break;
    }
    }
    break;
  }
  digitalWrite(13, 0);
}
