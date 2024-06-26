# Very partial mapping of keys to keycodes for the linux input subsystem.
# Source: man virkeycode-linux(7)
keys = {
    # "": 0x0,  # KEY_RESERVED
    # "": 0x1,  # KEY_ESC
    "1": 0x2,  # KEY_1
    "2": 0x3,  # KEY_2
    "3": 0x4,  # KEY_3
    "4": 0x5,  # KEY_4
    "5": 0x6,  # KEY_5
    "6": 0x7,  # KEY_6
    "7": 0x8,  # KEY_7
    "8": 0x9,  # KEY_8
    "9": 0xA,  # KEY_9
    "0": 0xB,  # KEY_0
    # "": 0xc,  # KEY_MINUS
    # "": 0xd,  # KEY_EQUAL
    # "": 0xe,  # KEY_BACKSPACE
    # "": 0xf,  # KEY_TAB
    "Q": 0x10,  # KEY_Q
    "W": 0x11,  # KEY_W
    "E": 0x12,  # KEY_E
    "R": 0x13,  # KEY_R
    "T": 0x14,  # KEY_T
    "Y": 0x15,  # KEY_Y
    "U": 0x16,  # KEY_U
    "I": 0x17,  # KEY_I
    "O": 0x18,  # KEY_O
    "P": 0x19,  # KEY_P
    # "": 0x1a,  # KEY_LEFTBRACE
    # "": 0x1b,  # KEY_RIGHTBRACE
    "\n": 0x1C,  # KEY_ENTER
    # "": 0x1d,  # KEY_LEFTCTRL
    "A": 0x1E,  # KEY_A
    "S": 0x1F,  # KEY_S
    "D": 0x20,  # KEY_D
    "F": 0x21,  # KEY_F
    "G": 0x22,  # KEY_G
    "H": 0x23,  # KEY_H
    "J": 0x24,  # KEY_J
    "K": 0x25,  # KEY_K
    "L": 0x26,  # KEY_L
    # "": 0x27,  # KEY_SEMICOLON
    # "": 0x28,  # KEY_APOSTROPHE
    # "": 0x29,  # KEY_GRAVE
    # "": 0x2a,  # KEY_LEFTSHIFT
    # "": 0x2b,  # KEY_BACKSLASH
    "Z": 0x2C,  # KEY_Z
    "X": 0x2D,  # KEY_X
    "C": 0x2E,  # KEY_C
    "V": 0x2F,  # KEY_V
    "B": 0x30,  # KEY_B
    "N": 0x31,  # KEY_N
    "M": 0x32,  # KEY_M
    # "": 0x33,  # KEY_COMMA
    # "": 0x34,  # KEY_DOT
    # "": 0x35,  # KEY_SLASH
    # "": 0x36,  # KEY_RIGHTSHIFT
    # "": 0x37,  # KEY_KPASTERISK
    # "": 0x38,  # KEY_LEFTALT
    # "": 0x39,  # KEY_SPACE
    # "": 0x3a,  # KEY_CAPSLOCK
    # "": 0x3b,  # KEY_F1
    # "": 0x3c,  # KEY_F2
    # "": 0x3d,  # KEY_F3
    # "": 0x3e,  # KEY_F4
    # "": 0x3f,  # KEY_F5
    # "": 0x40,  # KEY_F6
    # "": 0x41,  # KEY_F7
    # "": 0x42,  # KEY_F8
    # "": 0x43,  # KEY_F9
    # "": 0x44,  # KEY_F10
    # "": 0x45,  # KEY_NUMLOCK
    # "": 0x46,  # KEY_SCROLLLOCK
    # "": 0x47,  # KEY_KP7
    # "": 0x48,  # KEY_KP8
    # "": 0x49,  # KEY_KP9
    # "": 0x4a,  # KEY_KPMINUS
    # "": 0x4b,  # KEY_KP4
    # "": 0x4c,  # KEY_KP5
    # "": 0x4d,  # KEY_KP6
    # "": 0x4e,  # KEY_KPPLUS
    # "": 0x4f,  # KEY_KP1
    # "": 0x50,  # KEY_KP2
    # "": 0x51,  # KEY_KP3
    # "": 0x52,  # KEY_KP0
    # "": 0x53,  # KEY_KPDOT
    # "": 0x54,  # unnamed
    # "": 0x55,  # KEY_ZENKAKUHANKAKU
    # "": 0x56,  # KEY_102ND
    # "": 0x57,  # KEY_F11
    # "": 0x58,  # KEY_F12
    # "": 0x59,  # KEY_RO
    # "": 0x5a,  # KEY_KATAKANA
    # "": 0x5b,  # KEY_HIRAGANA
    # "": 0x5c,  # KEY_HENKAN
    # "": 0x5d,  # KEY_KATAKANAHIRAGANA
    # "": 0x5e,  # KEY_MUHENKAN
    # "": 0x5f,  # KEY_KPJPCOMMA
    # "": 0x60,  # KEY_KPENTER
    # "": 0x61,  # KEY_RIGHTCTRL
    # "": 0x62,  # KEY_KPSLASH
    # "": 0x63,  # KEY_SYSRQ
    # "": 0x64,  # KEY_RIGHTALT
    # "": 0x65,  # KEY_LINEFEED
    # "": 0x66,  # KEY_HOME
    # "": 0x67,  # KEY_UP
    # "": 0x68,  # KEY_PAGEUP
    # "": 0x69,  # KEY_LEFT
    # "": 0x6a,  # KEY_RIGHT
    # "": 0x6b,  # KEY_END
    # "": 0x6c,  # KEY_DOWN
    # "": 0x6d,  # KEY_PAGEDOWN
    # "": 0x6e,  # KEY_INSERT
    # "": 0x6f,  # KEY_DELETE
    # "": 0x70,  # KEY_MACRO
    # "": 0x71,  # KEY_MUTE
    # "": 0x72,  # KEY_VOLUMEDOWN
    # "": 0x73,  # KEY_VOLUMEUP
    # "": 0x74,  # KEY_POWER
    # "": 0x75,  # KEY_KPEQUAL
    # "": 0x76,  # KEY_KPPLUSMINUS
    # "": 0x77,  # KEY_PAUSE
    # "": 0x78,  # KEY_SCALE
    # "": 0x79,  # KEY_KPCOMMA
    # "": 0x7a,  # KEY_HANGEUL
    # "": 0x7b,  # KEY_HANJA
    # "": 0x7c,  # KEY_YEN
    # "": 0x7d,  # KEY_LEFTMETA
    # "": 0x7e,  # KEY_RIGHTMETA
    # "": 0x7f,  # KEY_COMPOSE
    # "": 0x80,  # KEY_STOP
    # "": 0x81,  # KEY_AGAIN
    # "": 0x82,  # KEY_PROPS
    # "": 0x83,  # KEY_UNDO
    # "": 0x84,  # KEY_FRONT
    # "": 0x85,  # KEY_COPY
    # "": 0x86,  # KEY_OPEN
    # "": 0x87,  # KEY_PASTE
    # "": 0x88,  # KEY_FIND
    # "": 0x89,  # KEY_CUT
    # "": 0x8a,  # KEY_HELP
    # "": 0x8b,  # KEY_MENU
    # "": 0x8c,  # KEY_CALC
    # "": 0x8d,  # KEY_SETUP
    # "": 0x8e,  # KEY_SLEEP
    # "": 0x8f,  # KEY_WAKEUP
    # "": 0x90,  # KEY_FILE
    # "": 0x91,  # KEY_SENDFILE
    # "": 0x92,  # KEY_DELETEFILE
    # "": 0x93,  # KEY_XFER
    # "": 0x94,  # KEY_PROG1
    # "": 0x95,  # KEY_PROG2
    # "": 0x96,  # KEY_WWW
    # "": 0x97,  # KEY_MSDOS
    # "": 0x98,  # KEY_SCREENLOCK
    # "": 0x99,  # KEY_DIRECTION
    # "": 0x9a,  # KEY_CYCLEWINDOWS
    # "": 0x9b,  # KEY_MAIL
    # "": 0x9c,  # KEY_BOOKMARKS
    # "": 0x9d,  # KEY_COMPUTER
    # "": 0x9e,  # KEY_BACK
    # "": 0x9f,  # KEY_FORWARD
    # "": 0xa0,  # KEY_CLOSECD
    # "": 0xa1,  # KEY_EJECTCD
    # "": 0xa2,  # KEY_EJECTCLOSECD
    # "": 0xa3,  # KEY_NEXTSONG
    # "": 0xa4,  # KEY_PLAYPAUSE
    # "": 0xa5,  # KEY_PREVIOUSSONG
    # "": 0xa6,  # KEY_STOPCD
    # "": 0xa7,  # KEY_RECORD
    # "": 0xa8,  # KEY_REWIND
    # "": 0xa9,  # KEY_PHONE
    # "": 0xaa,  # KEY_ISO
    # "": 0xab,  # KEY_CONFIG
    # "": 0xac,  # KEY_HOMEPAGE
    # "": 0xad,  # KEY_REFRESH
    # "": 0xae,  # KEY_EXIT
    # "": 0xaf,  # KEY_MOVE
    # "": 0xb0,  # KEY_EDIT
    # "": 0xb1,  # KEY_SCROLLUP
    # "": 0xb2,  # KEY_SCROLLDOWN
    # "": 0xb3,  # KEY_KPLEFTPAREN
    # "": 0xb4,  # KEY_KPRIGHTPAREN
    # "": 0xb5,  # KEY_NEW
    # "": 0xb6,  # KEY_REDO
    # "": 0xb7,  # KEY_F13
    # "": 0xb8,  # KEY_F14
    # "": 0xb9,  # KEY_F15
    # "": 0xba,  # KEY_F16
    # "": 0xbb,  # KEY_F17
    # "": 0xbc,  # KEY_F18
    # "": 0xbd,  # KEY_F19
    # "": 0xbe,  # KEY_F20
    # "": 0xbf,  # KEY_F21
    # "": 0xc0,  # KEY_F22
    # "": 0xc1,  # KEY_F23
    # "": 0xc2,  # KEY_F24
    # "": 0xc3,  # unnamed
    # "": 0xc4,  # unnamed
    # "": 0xc5,  # unnamed
    # "": 0xc6,  # unnamed
    # "": 0xc7,  # unnamed
    # "": 0xc8,  # KEY_PLAYCD
    # "": 0xc9,  # KEY_PAUSECD
    # "": 0xca,  # KEY_PROG3
    # "": 0xcb,  # KEY_PROG4
    # "": 0xcc,  # KEY_DASHBOARD
    # "": 0xcd,  # KEY_SUSPEND
    # "": 0xce,  # KEY_CLOSE
    # "": 0xcf,  # KEY_PLAY
    # "": 0xd0,  # KEY_FASTFORWARD
    # "": 0xd1,  # KEY_BASSBOOST
    # "": 0xd2,  # KEY_PRINT
    # "": 0xd3,  # KEY_HP
    # "": 0xd4,  # KEY_CAMERA
    # "": 0xd5,  # KEY_SOUND
    # "": 0xd6,  # KEY_QUESTION
    # "": 0xd7,  # KEY_EMAIL
    # "": 0xd8,  # KEY_CHAT
    # "": 0xd9,  # KEY_SEARCH
    # "": 0xda,  # KEY_CONNECT
    # "": 0xdb,  # KEY_FINANCE
    # "": 0xdc,  # KEY_SPORT
    # "": 0xdd,  # KEY_SHOP
    # "": 0xde,  # KEY_ALTERASE
    # "": 0xdf,  # KEY_CANCEL
    # "": 0xe0,  # KEY_BRIGHTNESSDOWN
    # "": 0xe1,  # KEY_BRIGHTNESSUP
    # "": 0xe2,  # KEY_MEDIA
    # "": 0xe3,  # KEY_SWITCHVIDEOMODE
    # "": 0xe4,  # KEY_KBDILLUMTOGGLE
    # "": 0xe5,  # KEY_KBDILLUMDOWN
    # "": 0xe6,  # KEY_KBDILLUMUP
    # "": 0xe7,  # KEY_SEND
    # "": 0xe8,  # KEY_REPLY
    # "": 0xe9,  # KEY_FORWARDMAIL
    # "": 0xea,  # KEY_SAVE
    # "": 0xeb,  # KEY_DOCUMENTS
    # "": 0xec,  # KEY_BATTERY
    # "": 0xed,  # KEY_BLUETOOTH
    # "": 0xee,  # KEY_WLAN
    # "": 0xef,  # KEY_UWB
    # "": 0xf0,  # KEY_UNKNOWN
    # "": 0xf1,  # KEY_VIDEO_NEXT
    # "": 0xf2,  # KEY_VIDEO_PREV
    # "": 0xf3,  # KEY_BRIGHTNESS_CYCLE
    # "": 0xf4,  # KEY_BRIGHTNESS_ZERO
    # "": 0xf5,  # KEY_DISPLAY_OFF
    # "": 0xf6,  # KEY_WIMAX
    # "": 0xf7,  # unnamed
    # "": 0xf8,  # unnamed
    # "": 0xf9,  # unnamed
    # "": 0xfa,  # unnamed
    # "": 0xfb,  # unnamed
    # "": 0xfc,  # unnamed
    # "": 0xfd,  # unnamed
    # "": 0xfe,  # unnamed
    # "": 0xff,  # unnamed
    # "": 0x100,  # BTN_0
    # "": 0x101,  # BTN_1
    # "": 0x102,  # BTN_2
    # "": 0x103,  # BTN_3
    # "": 0x104,  # BTN_4
    # "": 0x105,  # BTN_5
    # "": 0x106,  # BTN_6
    # "": 0x107,  # BTN_7
    # "": 0x108,  # BTN_8
    # "": 0x109,  # BTN_9
    # "": 0x110,  # BTN_LEFT
    # "": 0x111,  # BTN_RIGHT
    # "": 0x112,  # BTN_MIDDLE
    # "": 0x113,  # BTN_SIDE
    # "": 0x114,  # BTN_EXTRA
    # "": 0x115,  # BTN_FORWARD
    # "": 0x116,  # BTN_BACK
    # "": 0x117,  # BTN_TASK
    # "": 0x120,  # BTN_TRIGGER
    # "": 0x121,  # BTN_THUMB
    # "": 0x122,  # BTN_THUMB2
    # "": 0x123,  # BTN_TOP
    # "": 0x124,  # BTN_TOP2
    # "": 0x125,  # BTN_PINKIE
    # "": 0x126,  # BTN_BASE
    # "": 0x127,  # BTN_BASE2
    # "": 0x128,  # BTN_BASE3
    # "": 0x129,  # BTN_BASE4
    # "": 0x12a,  # BTN_BASE5
    # "": 0x12b,  # BTN_BASE6
    # "": 0x12f,  # BTN_DEAD
    # "": 0x130,  # BTN_A
    # "": 0x131,  # BTN_B
    # "": 0x132,  # BTN_C
    # "": 0x133,  # BTN_X
    # "": 0x134,  # BTN_Y
    # "": 0x135,  # BTN_Z
    # "": 0x136,  # BTN_TL
    # "": 0x137,  # BTN_TR
    # "": 0x138,  # BTN_TL2
    # "": 0x139,  # BTN_TR2
    # "": 0x13a,  # BTN_SELECT
    # "": 0x13b,  # BTN_START
    # "": 0x13c,  # BTN_MODE
    # "": 0x13d,  # BTN_THUMBL
    # "": 0x13e,  # BTN_THUMBR
    # "": 0x140,  # BTN_TOOL_PEN
    # "": 0x141,  # BTN_TOOL_RUBBER
    # "": 0x142,  # BTN_TOOL_BRUSH
    # "": 0x143,  # BTN_TOOL_PENCIL
    # "": 0x144,  # BTN_TOOL_AIRBRUSH
    # "": 0x145,  # BTN_TOOL_FINGER
    # "": 0x146,  # BTN_TOOL_MOUSE
    # "": 0x147,  # BTN_TOOL_LENS
    # "": 0x14a,  # BTN_TOUCH
    # "": 0x14b,  # BTN_STYLUS
    # "": 0x14c,  # BTN_STYLUS2
    # "": 0x14d,  # BTN_TOOL_DOUBLETAP
    # "": 0x14e,  # BTN_TOOL_TRIPLETAP
    # "": 0x14f,  # BTN_TOOL_QUADTAP
    # "": 0x150,  # BTN_GEAR_DOWN
    # "": 0x151,  # BTN_GEAR_UP
    # "": 0x160,  # KEY_OK
    # "": 0x161,  # KEY_SELECT
    # "": 0x162,  # KEY_GOTO
    # "": 0x163,  # KEY_CLEAR
    # "": 0x164,  # KEY_POWER2
    # "": 0x165,  # KEY_OPTION
    # "": 0x166,  # KEY_INFO
    # "": 0x167,  # KEY_TIME
    # "": 0x168,  # KEY_VENDOR
    # "": 0x169,  # KEY_ARCHIVE
    # "": 0x16a,  # KEY_PROGRAM
    # "": 0x16b,  # KEY_CHANNEL
    # "": 0x16c,  # KEY_FAVORITES
    # "": 0x16d,  # KEY_EPG
    # "": 0x16e,  # KEY_PVR
    # "": 0x16f,  # KEY_MHP
    # "": 0x170,  # KEY_LANGUAGE
    # "": 0x171,  # KEY_TITLE
    # "": 0x172,  # KEY_SUBTITLE
    # "": 0x173,  # KEY_ANGLE
    # "": 0x174,  # KEY_ZOOM
    # "": 0x175,  # KEY_MODE
    # "": 0x176,  # KEY_KEYBOARD
    # "": 0x177,  # KEY_SCREEN
    # "": 0x178,  # KEY_PC
    # "": 0x179,  # KEY_TV
    # "": 0x17a,  # KEY_TV2
    # "": 0x17b,  # KEY_VCR
    # "": 0x17c,  # KEY_VCR2
    # "": 0x17d,  # KEY_SAT
    # "": 0x17e,  # KEY_SAT2
    # "": 0x17f,  # KEY_CD
    # "": 0x180,  # KEY_TAPE
    # "": 0x181,  # KEY_RADIO
    # "": 0x182,  # KEY_TUNER
    # "": 0x183,  # KEY_PLAYER
    # "": 0x184,  # KEY_TEXT
    # "": 0x185,  # KEY_DVD
    # "": 0x186,  # KEY_AUX
    # "": 0x187,  # KEY_MP3
    # "": 0x188,  # KEY_AUDIO
    # "": 0x189,  # KEY_VIDEO
    # "": 0x18a,  # KEY_DIRECTORY
    # "": 0x18b,  # KEY_LIST
    # "": 0x18c,  # KEY_MEMO
    # "": 0x18d,  # KEY_CALENDAR
    # "": 0x18e,  # KEY_RED
    # "": 0x18f,  # KEY_GREEN
    # "": 0x190,  # KEY_YELLOW
    # "": 0x191,  # KEY_BLUE
    # "": 0x192,  # KEY_CHANNELUP
    # "": 0x193,  # KEY_CHANNELDOWN
    # "": 0x194,  # KEY_FIRST
    # "": 0x195,  # KEY_LAST
    # "": 0x196,  # KEY_AB
    # "": 0x197,  # KEY_NEXT
    # "": 0x198,  # KEY_RESTART
    # "": 0x199,  # KEY_SLOW
    # "": 0x19a,  # KEY_SHUFFLE
    # "": 0x19b,  # KEY_BREAK
    # "": 0x19c,  # KEY_PREVIOUS
    # "": 0x19d,  # KEY_DIGITS
    # "": 0x19e,  # KEY_TEEN
    # "": 0x19f,  # KEY_TWEN
    # "": 0x1a0,  # KEY_VIDEOPHONE
    # "": 0x1a1,  # KEY_GAMES
    # "": 0x1a2,  # KEY_ZOOMIN
    # "": 0x1a3,  # KEY_ZOOMOUT
    # "": 0x1a4,  # KEY_ZOOMRESET
    # "": 0x1a5,  # KEY_WORDPROCESSOR
    # "": 0x1a6,  # KEY_EDITOR
    # "": 0x1a7,  # KEY_SPREADSHEET
    # "": 0x1a8,  # KEY_GRAPHICSEDITOR
    # "": 0x1a9,  # KEY_PRESENTATION
    # "": 0x1aa,  # KEY_DATABASE
    # "": 0x1ab,  # KEY_NEWS
    # "": 0x1ac,  # KEY_VOICEMAIL
    # "": 0x1ad,  # KEY_ADDRESSBOOK
    # "": 0x1ae,  # KEY_MESSENGER
    # "": 0x1af,  # KEY_DISPLAYTOGGLE
    # "": 0x1b0,  # KEY_SPELLCHECK
    # "": 0x1b1,  # KEY_LOGOFF
    # "": 0x1b2,  # KEY_DOLLAR
    # "": 0x1b3,  # KEY_EURO
    # "": 0x1b4,  # KEY_FRAMEBACK
    # "": 0x1b5,  # KEY_FRAMEFORWARD
    # "": 0x1b6,  # KEY_CONTEXT_MENU
    # "": 0x1b7,  # KEY_MEDIA_REPEAT
    # "": 0x1c0,  # KEY_DEL_EOL
    # "": 0x1c1,  # KEY_DEL_EOS
    # "": 0x1c2,  # KEY_INS_LINE
    # "": 0x1c3,  # KEY_DEL_LINE
    # "": 0x1d0,  # KEY_FN
    # "": 0x1d1,  # KEY_FN_ESC
    # "": 0x1d2,  # KEY_FN_F1
    # "": 0x1d3,  # KEY_FN_F2
    # "": 0x1d4,  # KEY_FN_F3
    # "": 0x1d5,  # KEY_FN_F4
    # "": 0x1d6,  # KEY_FN_F5
    # "": 0x1d7,  # KEY_FN_F6
    # "": 0x1d8,  # KEY_FN_F7
    # "": 0x1d9,  # KEY_FN_F8
    # "": 0x1da,  # KEY_FN_F9
    # "": 0x1db,  # KEY_FN_F10
    # "": 0x1dc,  # KEY_FN_F11
    # "": 0x1dd,  # KEY_FN_F12
    # "": 0x1de,  # KEY_FN_1
    # "": 0x1df,  # KEY_FN_2
    # "": 0x1e0,  # KEY_FN_D
    # "": 0x1e1,  # KEY_FN_E
    # "": 0x1e2,  # KEY_FN_F
    # "": 0x1e3,  # KEY_FN_S
    # "": 0x1e4,  # KEY_FN_B
    # "": 0x1f1,  # KEY_BRL_DOT1
    # "": 0x1f2,  # KEY_BRL_DOT2
    # "": 0x1f3,  # KEY_BRL_DOT3
    # "": 0x1f4,  # KEY_BRL_DOT4
    # "": 0x1f5,  # KEY_BRL_DOT5
    # "": 0x1f6,  # KEY_BRL_DOT6
    # "": 0x1f7,  # KEY_BRL_DOT7
    # "": 0x1f8,  # KEY_BRL_DOT8
    # "": 0x1f9,  # KEY_BRL_DOT9
    # "": 0x1fa,  # KEY_BRL_DOT10
    # "": 0x200,  # KEY_NUMERIC_0
    # "": 0x201,  # KEY_NUMERIC_1
    # "": 0x202,  # KEY_NUMERIC_2
    # "": 0x203,  # KEY_NUMERIC_3
    # "": 0x204,  # KEY_NUMERIC_4
    # "": 0x205,  # KEY_NUMERIC_5
    # "": 0x206,  # KEY_NUMERIC_6
    # "": 0x207,  # KEY_NUMERIC_7
    # "": 0x208,  # KEY_NUMERIC_8
    # "": 0x209,  # KEY_NUMERIC_9
    # "": 0x20a,  # KEY_NUMERIC_STAR
    # "": 0x20b,  # KEY_NUMERIC_POUND
    # "": 0x20c,  # KEY_RFKILL
}
