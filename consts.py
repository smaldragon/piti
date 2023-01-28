VAR_REAL_NUM = 0x00
VAR_REAL_LIST = 0x01
VAR_MATRIX = 0x02
VAR_Y_VAR = 0x03
VAR_STRING = 0x04
VAR_PROGRAM = 0x05
VAR_PROGRAM_LOCKED = 0x06
VAR_PICTURE = 0x07
VAR_GDB = 0x08
VAR_WINDOW_SETTINGS_1 = 0x0B
VAR_COMPLEX_NUM = 0x0C
VAR_COMPLEX_LIST = 0x0D
VAR_WINDOW_SETTINGS_2 = 0x0F
VAR_WINDOW_SETTINGS_3 = 0x10
VAR_TABLE_SETUP = 0x11
VAR_BACKUP = 0x13
VAR_DELETE = 0x14
VAR_APP_VAR = 0x15
VAR_GROUP_VAR = 0x17
VAR_DIR = 0x19
VAR_FLASH_OS = 0x23
VAR_FLASH_APP = 0x24
VAR_ID_LIST = 0x26
VAR_CERTIFICATE = 0x27
VAR_CLOCK = 0x29

VAR_DESC = {
    VAR_REAL_NUM : "Real Number",
    VAR_REAL_LIST : "Real List",
    VAR_MATRIX : "Matrix",
    VAR_Y_VAR : "Y-Var",
    VAR_STRING : "String",
    VAR_PROGRAM : "Program",
    VAR_PROGRAM_LOCKED : "Program (locked)",
    VAR_PICTURE : "Picture",
    VAR_GDB : "GDB",
    VAR_WINDOW_SETTINGS_1 : "Window Settings",
    VAR_COMPLEX_NUM : "Complex Number",
    VAR_COMPLEX_LIST : "Complex List",
    VAR_WINDOW_SETTINGS_2 : "Window Settings",
    VAR_WINDOW_SETTINGS_3 : "Window Settings",
    VAR_TABLE_SETUP : "Table Setup",
    VAR_BACKUP : "Backup",
    VAR_DELETE : "Delete",
    VAR_APP_VAR : "App Variable",
    VAR_GROUP_VAR : "Group Variable",
    VAR_DIR : "Directory",
    VAR_FLASH_OS : "Flash OS",
    VAR_FLASH_APP : "Flash App",
    VAR_ID_LIST : "ID List",
    VAR_CERTIFICATE : "Certificate",
    VAR_CLOCK : "Clock"
}

VAR_EXT = {
    VAR_REAL_NUM : ".8xn",
    VAR_REAL_LIST : ".8xl",
    VAR_MATRIX : ".8xm",
    VAR_Y_VAR : ".8xy",
    VAR_STRING : ".8xs",
    VAR_PROGRAM : ".8xp",
    VAR_PROGRAM_LOCKED : ".8xp",
    VAR_PICTURE : ".8xi",
    VAR_GDB : ".8xd",
    VAR_WINDOW_SETTINGS_1 : ".8xw",
    VAR_COMPLEX_NUM : ".8xc",
    VAR_COMPLEX_LIST : ".8xl",
    VAR_WINDOW_SETTINGS_2 : ".8xw",
    VAR_WINDOW_SETTINGS_3 : ".8xw",
    VAR_TABLE_SETUP : ".8xt",
    VAR_BACKUP : ".8bak",	#TODO: replace with typical ext
    VAR_DELETE : "",
    VAR_APP_VAR : ".8xv",
    VAR_GROUP_VAR : ".8xgrp",
    VAR_DIR : "",
    VAR_FLASH_OS : ".8xu",
    VAR_FLASH_APP : ".8xk",
    VAR_ID_LIST : "",
    VAR_CERTIFICATE : ".8xq",
    VAR_CLOCK : ""
}

CMD_VAR = 0x06      # Variable Header
CMD_CTS = 0x09      # Clear to Send
CMD_DATA = 0x15     # Data
CMD_VER = 0x2D      # Request Versions
CMD_SKIP = 0x36     # Skip/Exit Comm
CMD_ACK = 0x56      # Acknoledge
CMD_ERR = 0x5A      # Error
CMD_ERR_EXIT = 0x01
CMD_ERR_SKIP = 0x02
CMD_ERR_MEM  = 0x03
CMD_RDY = 0x68      # Check Ready
CMD_SCR = 0x6D      # Request Screenshot
CMD_DEL = 0x88      # Delete Variable
CMD_EOT = 0x92      # End of Transmission
CMD_REQ = 0xA2      # Request Variable
CMD_RTS = 0xC9      # Request to Send


tokens = {
	#0x00
	0x01: "▸DMS",
	0x02: "▸Dec",
	0x03: "▸Frac",
	0x04: "→",
	0x05: "BoxPlot",
	0x06: "[",
	0x07: "]",
	0x08: "{",
	0x09: "}",
	0x0A: "ʳ",
	0x0B: "°",
	0x0C: "-1",
	0x0D: "2",
	0x0E: "T",
	0x0F: "3",
	
	0x10: "(",
	0x11: ")",
	0x12: "round(",
	0x13: "pxl-Test(",
	0x14: "augment(",
	0x15: "rowSwap(",
	0x16: "row+(",
	0x17: "*row(",
	0x18: "*row+(",
	0x19: "max(",
	0x1A: "min(",
	0x1B: "R▸Pr(",
	0x1C: "R▸Pθ(",
	0x1D: "P▸Rx(",
	0x1E: "P▸Ry(",
	0x1F: "median(",
	
	0x20: "randM(",
	0x21: "mean(",
	0x22: "solve(",
	0x23: "seq(",
	0x24: "fnInt(",
	0x25: "nDeriv(",
	#0x26
	0x27: "fMin(",
	0x28: "fMax(",
	
}
