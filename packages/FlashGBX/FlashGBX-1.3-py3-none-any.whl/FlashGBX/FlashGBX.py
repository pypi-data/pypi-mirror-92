# -*- coding: utf-8 -*-
# ＵＴＦ－８
import sys, threading, os, glob, time, re, json, platform, subprocess, zlib, argparse, math, struct, statistics, requests, webbrowser, pkg_resources
from PySide2 import QtCore, QtWidgets, QtGui
from zipfile import *
from datetime import datetime
from .RomFileDMG import *
from .RomFileAGB import *
from .PocketCamera import *
from . import hw_GBxCartRW
hw_devices = [hw_GBxCartRW]

APPNAME = "FlashGBX"
VERSION_PEP440 = "1.3"
VERSION = "v{:s}".format(VERSION_PEP440)

class FlashGBX(QtWidgets.QWidget):
	global APPNAME, VERSION, VERSION_PEP440
	
	AGB_Header_ROM_Sizes = [ "4 MB", "8 MB", "16 MB", "32 MB" ]
	AGB_Header_ROM_Sizes_Map = [ 0x400000, 0x800000, 0x1000000, 0x2000000 ]
	AGB_Header_Save_Types = [ "None", "4K EEPROM (512 Bytes)", "64K EEPROM (8 KB)", "256K SRAM (32 KB)", "512K SRAM (64 KB)", "1M SRAM (128 KB)", "512K FLASH (64 KB)", "1M FLASH (128 KB)" ]
	AGB_Global_CRC32 = 0
	
	DMG_Header_Features = { 0x00:'ROM ONLY', 0x01:'MBC1', 0x02:'MBC1+RAM', 0x03:'MBC1+RAM+BATTERY', 0x05:'MBC2', 0x06:'MBC2+BATTERY', 0x08:'ROM+RAM', 0x09:'ROM+RAM+BATTERY', 0x0B:'MMM01', 0x0C:'MMM01+RAM', 0x0D:'MMM01+RAM+BATTERY', 0x0F:'MBC3+TIMER+BATTERY', 0x10:'MBC3+TIMER+RAM+BATTERY', 0x11:'MBC3', 0x12:'MBC3+RAM', 0x13:'MBC3+RAM+BATTERY', 0x15:'MBC4', 0x16:'MBC4+RAM', 0x17:'MBC4+RAM+BATTERY', 0x19:'MBC5', 0x1A:'MBC5+RAM', 0x1B:'MBC5+RAM+BATTERY', 0x1C:'MBC5+RUMBLE', 0x1D:'MBC5+RUMBLE+RAM', 0x1E:'MBC5+RUMBLE+RAM+BATTERY', 0x20:'MBC6', 0x22:'MBC7+RAM+BATTERY', 0x55:'Game Genie', 0x56:'Game Genie v3.0', 0xFC:'POCKET CAMERA', 0xFD:'BANDAI TAMA5', 0xFE:'HuC3', 0xFF:'HuC1+RAM+BATTERY' }
	DMG_Header_Features_MBC = [ 0, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 7, 0, 0, 0, 0, 0, 0 ]
	DMG_Header_ROM_Sizes = [ "32 KB", "64 KB", "128 KB", "256 KB", "512 KB", "1 MB", "1.1 MB", "1.2 MB", "1.5 MB", "2 MB", "4 MB", "8 MB" ]
	DMG_Header_ROM_Sizes_Map = [ 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x52, 0x53, 0x54, 0x06, 0x07, 0x08 ]
	DMG_Header_ROM_Sizes_Flasher_Map = [ 2, 4, 8, 16, 32, 64, 72, 80, 96, 128, 256, 512 ] # Number of ROM banks
	DMG_Header_RAM_Sizes = [ "None", "4K SRAM (512 Bytes)", "16K SRAM (2 KB)", "64K SRAM (8 KB)", "256K SRAM (32 KB)", "512K SRAM (64 KB)", "1M SRAM (128 KB)" ]
	DMG_Header_RAM_Sizes_Map = [ 0x00, 0x01, 0x01, 0x02, 0x03, 0x05, 0x04 ]
	DMG_Header_RAM_Sizes_Flasher_Map = [ 0, 0x200, 0x800, 0x2000, 0x8000, 0x10000, 0x20000 ] # RAM size in bytes
	DMG_Header_SGB = { 0x00:'No support', 0x03:'Supported' }
	DMG_Header_CGB = { 0x00:'No support', 0x80:'Supported', 0xC0:'Required' }
	
	CONN = None
	SETTINGS = None
	DEVICES = {}
	FLASHCARTS = { "DMG":{}, "AGB":{} }
	CONFIG_PATH = ""
	TBPROG = None # Windows 7+ Taskbar Progress Bar
	PROGRESS = {}
	MUTEX = threading.Lock()
	
	def __init__(self, args):
		app_path = args['app_path']
		QtWidgets.QWidget.__init__(self)
		self.setStyleSheet("QMessageBox { messagebox-text-interaction-flags: 5; }")
		self.setWindowIcon(QtGui.QIcon(app_path + "/res/icon.ico"))
		self.setWindowTitle("{:s} {:s}".format(APPNAME, VERSION))
		if hasattr(QtGui, "Qt"):
			self.setWindowFlags(self.windowFlags() | QtGui.Qt.MSWindowsFixedSizeDialogHint)
		
		# Create the QtWidgets.QVBoxLayout that lays out the whole form
		self.layout = QtWidgets.QGridLayout()
		self.layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
		self.layout_left = QtWidgets.QVBoxLayout()
		self.layout_right = QtWidgets.QVBoxLayout()
		self.layout.setContentsMargins(-1, 8, -1, 8)

		# Cartridge Information GroupBox
		self.grpDMGCartridgeInfo = self.GuiCreateGroupBoxDMGCartInfo()
		self.grpAGBCartridgeInfo = self.GuiCreateGroupBoxAGBCartInfo()
		self.grpAGBCartridgeInfo.setVisible(False)
		self.layout_left.addWidget(self.grpDMGCartridgeInfo)
		self.layout_left.addWidget(self.grpAGBCartridgeInfo)

		# Actions
		self.grpActions = QtWidgets.QGroupBox("Options")
		self.grpActionsLayout = QtWidgets.QVBoxLayout()
		self.grpActionsLayout.setContentsMargins(-1, 3, -1, -1)
		
		rowActionsMode = QtWidgets.QHBoxLayout()
		self.lblMode = QtWidgets.QLabel("Mode: ")
		rowActionsMode.addWidget(self.lblMode)
		self.optDMG = QtWidgets.QRadioButton("&Game Boy")
		self.connect(self.optDMG, QtCore.SIGNAL("clicked()"), self.SetMode)
		self.optAGB = QtWidgets.QRadioButton("Game Boy &Advance")
		self.connect(self.optAGB, QtCore.SIGNAL("clicked()"), self.SetMode)
		rowActionsMode.addWidget(self.optDMG)
		rowActionsMode.addWidget(self.optAGB)
		
		rowActionsGeneral1 = QtWidgets.QHBoxLayout()
		self.btnHeaderRefresh = QtWidgets.QPushButton("Read &Information")
		self.btnHeaderRefresh.setStyleSheet("min-height: 17px;")
		self.connect(self.btnHeaderRefresh, QtCore.SIGNAL("clicked()"), self.ReadCartridge)
		rowActionsGeneral1.addWidget(self.btnHeaderRefresh)

		rowActionsGeneral2 = QtWidgets.QHBoxLayout()
		self.btnBackupROM = QtWidgets.QPushButton("Backup &ROM")
		self.btnBackupROM.setStyleSheet("min-height: 17px;")
		self.connect(self.btnBackupROM, QtCore.SIGNAL("clicked()"), self.BackupROM)
		rowActionsGeneral2.addWidget(self.btnBackupROM)
		self.btnBackupRAM = QtWidgets.QPushButton("Backup &Save Data")
		self.btnBackupRAM.setStyleSheet("min-height: 17px;")
		self.connect(self.btnBackupRAM, QtCore.SIGNAL("clicked()"), self.BackupRAM)
		rowActionsGeneral2.addWidget(self.btnBackupRAM)
		
		self.cmbDMGCartridgeTypeResult.currentIndexChanged.connect(self.CartridgeTypeChanged)
		
		rowActionsGeneral3 = QtWidgets.QHBoxLayout()
		self.btnFlashROM = QtWidgets.QPushButton("&Flash ROM")
		self.btnFlashROM.setStyleSheet("min-height: 17px;")
		self.connect(self.btnFlashROM, QtCore.SIGNAL("clicked()"), self.FlashROM)
		rowActionsGeneral3.addWidget(self.btnFlashROM)
		self.btnRestoreRAM = QtWidgets.QPushButton("Writ&e Save Data")
		self.mnuRestoreRAM = QtWidgets.QMenu()
		self.mnuRestoreRAM.addAction("&Restore from save data file", self.WriteRAM)
		self.mnuRestoreRAM.addAction("&Erase cartridge save data", lambda: self.WriteRAM(erase=True))
		self.btnRestoreRAM.setMenu(self.mnuRestoreRAM)
		self.btnRestoreRAM.setStyleSheet("min-height: 17px;")
		rowActionsGeneral3.addWidget(self.btnRestoreRAM)

		self.grpActionsLayout.setSpacing(4)
		self.grpActionsLayout.addLayout(rowActionsMode)
		self.grpActionsLayout.addLayout(rowActionsGeneral1)
		self.grpActionsLayout.addLayout(rowActionsGeneral2)
		self.grpActionsLayout.addLayout(rowActionsGeneral3)
		self.grpActions.setLayout(self.grpActionsLayout)

		self.layout_right.addWidget(self.grpActions)

		# Transfer Status
		self.grpStatus = QtWidgets.QGroupBox("Transfer Status")
		grpStatusLayout = QtWidgets.QVBoxLayout()
		grpStatusLayout.setContentsMargins(-1, 3, -1, -1)

		rowStatus1a = QtWidgets.QHBoxLayout()
		self.lblStatus1a = QtWidgets.QLabel("Data transferred:")
		rowStatus1a.addWidget(self.lblStatus1a)
		self.lblStatus1aResult = QtWidgets.QLabel("–")
		rowStatus1a.addWidget(self.lblStatus1aResult)
		grpStatusLayout.addLayout(rowStatus1a)
		rowStatus2a = QtWidgets.QHBoxLayout()
		self.lblStatus2a = QtWidgets.QLabel("Transfer rate:")
		rowStatus2a.addWidget(self.lblStatus2a)
		self.lblStatus2aResult = QtWidgets.QLabel("–")
		rowStatus2a.addWidget(self.lblStatus2aResult)
		grpStatusLayout.addLayout(rowStatus2a)
		rowStatus3a = QtWidgets.QHBoxLayout()
		self.lblStatus3a = QtWidgets.QLabel("Time elapsed:")
		rowStatus3a.addWidget(self.lblStatus3a)
		self.lblStatus3aResult = QtWidgets.QLabel("–")
		rowStatus3a.addWidget(self.lblStatus3aResult)
		grpStatusLayout.addLayout(rowStatus3a)
		rowStatus4a = QtWidgets.QHBoxLayout()
		self.lblStatus4a = QtWidgets.QLabel("Ready.")
		rowStatus4a.addWidget(self.lblStatus4a)
		self.lblStatus4aResult = QtWidgets.QLabel("")
		rowStatus4a.addWidget(self.lblStatus4aResult)
		grpStatusLayout.addLayout(rowStatus4a)

		rowStatus2 = QtWidgets.QHBoxLayout()
		self.prgStatus = QtWidgets.QProgressBar()
		self.SetProgressBars(min=0, max=1, value=0)
		rowStatus2.addWidget(self.prgStatus)
		btnText = "Stop"
		self.btnCancel = QtWidgets.QPushButton(btnText)
		self.btnCancel.setEnabled(False)
		btnWidth = self.btnCancel.fontMetrics().boundingRect(btnText).width() + 15
		if platform.system() == "Darwin": btnWidth += 12
		self.btnCancel.setMaximumWidth(btnWidth)
		self.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), self.AbortOperation)
		rowStatus2.addWidget(self.btnCancel)

		grpStatusLayout.addLayout(rowStatus2)
		self.grpStatus.setLayout(grpStatusLayout)

		self.layout_right.addWidget(self.grpStatus)

		self.layout.addLayout(self.layout_left, 0, 0)
		self.layout.addLayout(self.layout_right, 0, 1)
		
		# List devices
		self.layout_devices = QtWidgets.QHBoxLayout()
		self.lblDevice = QtWidgets.QLabel()
		self.cmbDevice = QtWidgets.QComboBox()
		self.cmbDevice.setStyleSheet("QComboBox { border: 0; margin: 0; padding: 0; max-width: 0px; }");
		self.layout_devices.addWidget(self.lblDevice)
		self.layout_devices.addWidget(self.cmbDevice)
		self.layout_devices.addStretch()
		
		self.btnCameraViewer = QtWidgets.QPushButton("GB &Camera")
		self.connect(self.btnCameraViewer, QtCore.SIGNAL("clicked()"), self.ShowPocketCameraWindow)
		#rowActionsGeneral1.addWidget(self.btnCameraViewer)
		
		btnText = "C&onfig"
		self.btnConfig = QtWidgets.QPushButton(btnText)
		btnWidth = self.btnConfig.fontMetrics().boundingRect(btnText).width() + 24
		if platform.system() == "Darwin": btnWidth += 12
		self.btnConfig.setMaximumWidth(btnWidth)
		self.mnuConfig = QtWidgets.QMenu()
		self.mnuConfig.addAction("Check for &updates at application startup", lambda: [ self.SETTINGS.setValue("UpdateCheck", str(self.mnuConfig.actions()[0].isChecked()).lower().replace("true", "enabled").replace("false", "disabled")), self.UpdateCheck() ])
		self.mnuConfig.addAction("&Append date && time to filename of save data backups", lambda: self.SETTINGS.setValue("SaveFileNameAddDateTime", str(self.mnuConfig.actions()[1].isChecked()).lower().replace("true", "enabled").replace("false", "disabled")))
		self.mnuConfig.addAction("Prefer &sector erase over full chip erase when both available", lambda: self.SETTINGS.setValue("PreferSectorErase", str(self.mnuConfig.actions()[2].isChecked()).lower().replace("true", "enabled").replace("false", "disabled")))
		self.mnuConfig.addAction("&Verify flash after writing", lambda: self.SETTINGS.setValue("VerifyFlash", str(self.mnuConfig.actions()[3].isChecked()).lower().replace("true", "enabled").replace("false", "disabled")))
		self.mnuConfig.addAction("Use &fast read mode (experimental)", lambda: self.SETTINGS.setValue("FastReadMode", str(self.mnuConfig.actions()[4].isChecked()).lower().replace("true", "enabled").replace("false", "disabled"))) # GBxCart RW
		self.mnuConfig.addSeparator()
		self.mnuConfig.addAction("Show &configuration directory", self.OpenConfigDir)
		self.mnuConfig.actions()[0].setCheckable(True)
		self.mnuConfig.actions()[1].setCheckable(True)
		self.mnuConfig.actions()[2].setCheckable(True)
		self.mnuConfig.actions()[3].setCheckable(True)
		self.mnuConfig.actions()[4].setCheckable(True) # GBxCart RW
		self.btnConfig.setMenu(self.mnuConfig)
		
		#self.btnScan = QtWidgets.QPushButton("&Device Scan")
		#self.connect(self.btnScan, QtCore.SIGNAL("clicked()"), self.FindDevices)
		self.btnConnect = QtWidgets.QPushButton("&Connect")
		self.connect(self.btnConnect, QtCore.SIGNAL("clicked()"), self.ConnectDevice)
		self.layout_devices.addWidget(self.btnCameraViewer)
		self.layout_devices.addWidget(self.btnConfig)
		#self.layout_devices.addWidget(self.btnScan)
		self.layout_devices.addWidget(self.btnConnect)
		
		self.layout.addLayout(self.layout_devices, 1, 0, 1, 0)
		
		# Disable widgets
		self.optAGB.setEnabled(False)
		self.optDMG.setEnabled(False)
		self.btnHeaderRefresh.setEnabled(False)
		self.btnBackupROM.setEnabled(False)
		self.btnFlashROM.setEnabled(False)
		self.btnBackupRAM.setEnabled(False)
		self.btnRestoreRAM.setEnabled(False)
		self.btnConnect.setEnabled(False)
		self.grpDMGCartridgeInfo.setEnabled(False)
		self.grpAGBCartridgeInfo.setEnabled(False)
		
		# Set the VBox layout as the window's main layout
		self.setLayout(self.layout)
		
		# Read config, find devices and connect
		self.InitConfig(args)
		
		# Show app window first, then do update check
		qt_app.processEvents()
		QtCore.QTimer.singleShot(1, lambda: [ self.UpdateCheck(), self.FindDevices() ])
	
	def InitConfig(self, args):
		app_path = args['app_path']
		self.CONFIG_PATH = args['config_path']
		
		# Settings and Config
		deprecated_files = [ "fc_AGB_M36L0R705.txt", "config.ini" ]
		(config_version, fc_files) = self.ReadConfig(reset=args['argparsed'].reset)
		if config_version != VERSION:
			# Rename old files that have since been replaced/renamed/merged
			deprecated_files = [ "fc_AGB_M36L0R705.txt", "fc_AGB_TEST.txt", "fc_DMG_TEST.txt", "fc_AGB_Nintendo_E201850.txt", "fc_AGB_Nintendo_E201868.txt", "config.ini" ]
			for file in deprecated_files:
				if os.path.exists(self.CONFIG_PATH + "/" + file):
					os.rename(self.CONFIG_PATH + "/" + file, self.CONFIG_PATH + "/" + file + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".bak")
			
			rf_list = ""
			if os.path.exists(app_path + "/res/config.zip"):
				with ZipFile(app_path + "/res/config.zip") as zip:
					for zfile in zip.namelist():
						if os.path.exists(self.CONFIG_PATH + "/" + zfile):
							zfile_crc = zip.getinfo(zfile).CRC
							with open(self.CONFIG_PATH + "/" + zfile, "rb") as ofile: buffer = ofile.read()
							ofile_crc = zlib.crc32(buffer) & 0xFFFFFFFF
							if zfile_crc == ofile_crc: continue
							os.rename(self.CONFIG_PATH + "/" + zfile, self.CONFIG_PATH + "/" + zfile + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".bak")
							rf_list += zfile + "\n"
						zip.extract(zfile, self.CONFIG_PATH + "/")
				
				if rf_list != "": QtWidgets.QMessageBox.information(self, "{:s} {:s}".format(APPNAME, VERSION), "The application was recently updated and some config files have been updated as well. You will find backup copies of them in your configuration directory.\n\nUpdated files:\n" + rf_list[:-1], QtWidgets.QMessageBox.Ok)
				fc_files = glob.glob("{0:s}/fc_*.txt".format(self.CONFIG_PATH))
			else:
				print("WARNING: {:s} not found. This is required to load new flash cartridge type configurations after updating.\n".format(app_path + "/res/config.zip"))
		
		# Read flash cart types
		for file in fc_files:
			with open(file, encoding='utf-8') as f:
				data = f.read()
				specs_int = re.sub("(0x[\dA-F]+)", lambda m: str(int(m.group(1), 16)), data) # hex numbers to int numbers, otherwise not valid json
				try:
					specs = json.loads(specs_int)
				except:
					print("WARNING: Flash chip config file “{:s}” could not be parsed and needs to be fixed before it can be used.".format(os.path.basename(file)))
					continue
				for name in specs["names"]:
					if not specs["type"] in self.FLASHCARTS: continue # only DMG and AGB are supported right now
					self.FLASHCARTS[specs["type"]][name] = specs
		
		self.mnuConfig.actions()[0].setChecked(self.SETTINGS.value("UpdateCheck") == "enabled")
		self.mnuConfig.actions()[1].setChecked(self.SETTINGS.value("SaveFileNameAddDateTime") == "enabled")
		self.mnuConfig.actions()[2].setChecked(self.SETTINGS.value("PreferSectorErase") == "enabled")
		self.mnuConfig.actions()[3].setChecked(self.SETTINGS.value("VerifyFlash") == "enabled")
		self.mnuConfig.actions()[4].setChecked(self.SETTINGS.value("FastReadMode") == "enabled") # GBxCart RW
		
	def ReadConfig(self, reset=False):
		self.SETTINGS = QtCore.QSettings(self.CONFIG_PATH + "/settings.ini", QtCore.QSettings.IniFormat)
		config_version = self.SETTINGS.value("ConfigVersion")
		if not os.path.exists(self.CONFIG_PATH): os.makedirs(self.CONFIG_PATH)
		fc_files = glob.glob("{0:s}/fc_*.txt".format(self.CONFIG_PATH))
		if config_version is not None and len(fc_files) == 0:
			print("FAIL: No flash cartridge type configuration files found in {:s}. Resetting configuration...\n".format(self.CONFIG_PATH))
			self.SETTINGS.clear()
			os.rename(self.CONFIG_PATH + "/settings.ini", self.CONFIG_PATH + "/settings.ini_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".bak")
			config_version = False # extracts the config.zip again
		elif reset:
			self.SETTINGS.clear()
			print("All configuration has been reset.\n")
		
		self.SETTINGS.setValue("ConfigVersion", VERSION)
		return (config_version, fc_files)
	
	def GuiCreateGroupBoxDMGCartInfo(self):
		self.grpDMGCartridgeInfo = QtWidgets.QGroupBox("Game Boy Cartridge Information")
		self.grpDMGCartridgeInfo.setMinimumWidth(280)
		group_layout = QtWidgets.QVBoxLayout()
		group_layout.setContentsMargins(-1, 5, -1, -1)

		rowHeaderTitle = QtWidgets.QHBoxLayout()
		lblHeaderTitle = QtWidgets.QLabel("Game Title/Code:")
		lblHeaderTitle.setContentsMargins(0, 1, 0, 1)
		rowHeaderTitle.addWidget(lblHeaderTitle)
		self.lblHeaderTitleResult = QtWidgets.QLabel("")
		rowHeaderTitle.addWidget(self.lblHeaderTitleResult)
		group_layout.addLayout(rowHeaderTitle)

		rowHeaderSGB = QtWidgets.QHBoxLayout()
		lblHeaderSGB = QtWidgets.QLabel("Super Game Boy:")
		lblHeaderSGB.setContentsMargins(0, 1, 0, 1)
		rowHeaderSGB.addWidget(lblHeaderSGB)
		self.lblHeaderSGBResult = QtWidgets.QLabel("")
		rowHeaderSGB.addWidget(self.lblHeaderSGBResult)
		group_layout.addLayout(rowHeaderSGB)

		rowHeaderCGB = QtWidgets.QHBoxLayout()
		lblHeaderCGB = QtWidgets.QLabel("Game Boy Color:")
		lblHeaderCGB.setContentsMargins(0, 1, 0, 1)
		rowHeaderCGB.addWidget(lblHeaderCGB)
		self.lblHeaderCGBResult = QtWidgets.QLabel("")
		rowHeaderCGB.addWidget(self.lblHeaderCGBResult)
		group_layout.addLayout(rowHeaderCGB)

		rowHeaderLogoValid = QtWidgets.QHBoxLayout()
		lblHeaderLogoValid = QtWidgets.QLabel("Nintendo Logo:")
		lblHeaderLogoValid.setContentsMargins(0, 1, 0, 1)
		rowHeaderLogoValid.addWidget(lblHeaderLogoValid)
		self.lblHeaderLogoValidResult = QtWidgets.QLabel("")
		rowHeaderLogoValid.addWidget(self.lblHeaderLogoValidResult)
		group_layout.addLayout(rowHeaderLogoValid)

		rowHeaderChecksum = QtWidgets.QHBoxLayout()
		lblHeaderChecksum = QtWidgets.QLabel("Header Checksum:")
		lblHeaderChecksum.setContentsMargins(0, 1, 0, 1)
		rowHeaderChecksum.addWidget(lblHeaderChecksum)
		self.lblHeaderChecksumResult = QtWidgets.QLabel("")
		rowHeaderChecksum.addWidget(self.lblHeaderChecksumResult)
		group_layout.addLayout(rowHeaderChecksum)

		rowHeaderROMChecksum = QtWidgets.QHBoxLayout()
		lblHeaderROMChecksum = QtWidgets.QLabel("ROM Checksum:")
		lblHeaderROMChecksum.setContentsMargins(0, 1, 0, 1)
		rowHeaderROMChecksum.addWidget(lblHeaderROMChecksum)
		self.lblHeaderROMChecksumResult = QtWidgets.QLabel("")
		rowHeaderROMChecksum.addWidget(self.lblHeaderROMChecksumResult)
		group_layout.addLayout(rowHeaderROMChecksum)

		rowChipManufacturer = QtWidgets.QHBoxLayout()
		self.lblChipManufacturer = QtWidgets.QLabel("Chip Manufacturer:")
		self.lblChipManufacturer.setContentsMargins(0, 1, 0, 1)
		rowChipManufacturer.addWidget(self.lblChipManufacturer)
		self.lblChipManufacturerResult = QtWidgets.QLabel("")
		rowChipManufacturer.addWidget(self.lblChipManufacturerResult)
		group_layout.addLayout(rowChipManufacturer)
		self.lblChipManufacturer.setVisible(False)
		self.lblChipManufacturerResult.setVisible(False)

		rowChipID = QtWidgets.QHBoxLayout()
		self.lblChipID = QtWidgets.QLabel("Chip ID:")
		self.lblChipID.setContentsMargins(0, 1, 0, 1)
		rowChipID.addWidget(self.lblChipID)
		self.lblChipIDResult = QtWidgets.QLabel("")
		rowChipID.addWidget(self.lblChipIDResult)
		group_layout.addLayout(rowChipID)
		self.lblChipID.setVisible(False)
		self.lblChipIDResult.setVisible(False)

		rowHeaderROMSize = QtWidgets.QHBoxLayout()
		lblHeaderROMSize = QtWidgets.QLabel("ROM Size:")
		rowHeaderROMSize.addWidget(lblHeaderROMSize)
		self.cmbHeaderROMSizeResult = QtWidgets.QComboBox()
		self.cmbHeaderROMSizeResult.setStyleSheet("combobox-popup: 0;");
		self.cmbHeaderROMSizeResult.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.cmbHeaderROMSizeResult.addItems(self.DMG_Header_ROM_Sizes)
		self.cmbHeaderROMSizeResult.setCurrentIndex(self.cmbHeaderROMSizeResult.count() - 1)
		rowHeaderROMSize.addWidget(self.cmbHeaderROMSizeResult)
		group_layout.addLayout(rowHeaderROMSize)

		rowHeaderRAMSize = QtWidgets.QHBoxLayout()
		lblHeaderRAMSize = QtWidgets.QLabel("Save Type:")
		rowHeaderRAMSize.addWidget(lblHeaderRAMSize)
		self.cmbHeaderRAMSizeResult = QtWidgets.QComboBox()
		self.cmbHeaderRAMSizeResult.setStyleSheet("combobox-popup: 0;");
		self.cmbHeaderRAMSizeResult.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.cmbHeaderRAMSizeResult.addItems(self.DMG_Header_RAM_Sizes)
		self.cmbHeaderRAMSizeResult.setCurrentIndex(self.cmbHeaderRAMSizeResult.count() - 1)
		rowHeaderRAMSize.addWidget(self.cmbHeaderRAMSizeResult)
		group_layout.addLayout(rowHeaderRAMSize)

		rowHeaderFeatures = QtWidgets.QHBoxLayout()
		lblHeaderFeatures = QtWidgets.QLabel("Features:")
		rowHeaderFeatures.addWidget(lblHeaderFeatures)
		self.cmbHeaderFeaturesResult = QtWidgets.QComboBox()
		self.cmbHeaderFeaturesResult.setStyleSheet("combobox-popup: 0;");
		self.cmbHeaderFeaturesResult.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.cmbHeaderFeaturesResult.addItems(list(self.DMG_Header_Features.values()))
		rowHeaderFeatures.addWidget(self.cmbHeaderFeaturesResult)
		group_layout.addLayout(rowHeaderFeatures)

		rowCartridgeType = QtWidgets.QHBoxLayout()
		lblCartridgeType = QtWidgets.QLabel("Type:")
		rowCartridgeType.addWidget(lblCartridgeType)
		self.cmbDMGCartridgeTypeResult = QtWidgets.QComboBox()
		self.cmbDMGCartridgeTypeResult.setStyleSheet("max-width: 260px;")
		self.cmbDMGCartridgeTypeResult.setStyleSheet("combobox-popup: 0;");
		self.cmbDMGCartridgeTypeResult.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		rowCartridgeType.addWidget(self.cmbDMGCartridgeTypeResult)
		group_layout.addLayout(rowCartridgeType)

		self.grpDMGCartridgeInfo.setLayout(group_layout)
		
		return self.grpDMGCartridgeInfo
	
	def GuiCreateGroupBoxAGBCartInfo(self):
		self.grpAGBCartridgeInfo = QtWidgets.QGroupBox("Game Boy Advance Cartridge Information")
		self.grpAGBCartridgeInfo.setMinimumWidth(280)
		group_layout = QtWidgets.QVBoxLayout()
		group_layout.setContentsMargins(-1, 5, -1, -1)

		rowAGBHeaderTitle = QtWidgets.QHBoxLayout()
		lblAGBHeaderTitle = QtWidgets.QLabel("Game Title:")
		lblAGBHeaderTitle.setContentsMargins(0, 1, 0, 1)
		rowAGBHeaderTitle.addWidget(lblAGBHeaderTitle)
		self.lblAGBHeaderTitleResult = QtWidgets.QLabel("")
		rowAGBHeaderTitle.addWidget(self.lblAGBHeaderTitleResult)
		group_layout.addLayout(rowAGBHeaderTitle)

		rowAGBHeaderCode = QtWidgets.QHBoxLayout()
		lblAGBHeaderCode = QtWidgets.QLabel("Game Code:")
		lblAGBHeaderCode.setContentsMargins(0, 1, 0, 1)
		rowAGBHeaderCode.addWidget(lblAGBHeaderCode)
		self.lblAGBHeaderCodeResult = QtWidgets.QLabel("")
		rowAGBHeaderCode.addWidget(self.lblAGBHeaderCodeResult)
		group_layout.addLayout(rowAGBHeaderCode)

		rowAGBHeaderVersion = QtWidgets.QHBoxLayout()
		lblAGBHeaderVersion = QtWidgets.QLabel("Revision:")
		lblAGBHeaderVersion.setContentsMargins(0, 1, 0, 1)
		rowAGBHeaderVersion.addWidget(lblAGBHeaderVersion)
		self.lblAGBHeaderVersionResult = QtWidgets.QLabel("")
		rowAGBHeaderVersion.addWidget(self.lblAGBHeaderVersionResult)
		group_layout.addLayout(rowAGBHeaderVersion)

		rowAGBHeaderLogoValid = QtWidgets.QHBoxLayout()
		lblAGBHeaderLogoValid = QtWidgets.QLabel("Nintendo Logo:")
		lblAGBHeaderLogoValid.setContentsMargins(0, 1, 0, 1)
		rowAGBHeaderLogoValid.addWidget(lblAGBHeaderLogoValid)
		self.lblAGBHeaderLogoValidResult = QtWidgets.QLabel("")
		rowAGBHeaderLogoValid.addWidget(self.lblAGBHeaderLogoValidResult)
		group_layout.addLayout(rowAGBHeaderLogoValid)

		rowAGBHeader96h = QtWidgets.QHBoxLayout()
		lblAGBHeader96h = QtWidgets.QLabel("Cartridge Identifier:")
		lblAGBHeader96h.setContentsMargins(0, 1, 0, 1)
		rowAGBHeader96h.addWidget(lblAGBHeader96h)
		self.lblAGBHeader96hResult = QtWidgets.QLabel("")
		rowAGBHeader96h.addWidget(self.lblAGBHeader96hResult)
		group_layout.addLayout(rowAGBHeader96h)

		rowAGBHeaderChecksum = QtWidgets.QHBoxLayout()
		lblAGBHeaderChecksum = QtWidgets.QLabel("Header Checksum:")
		lblAGBHeaderChecksum.setContentsMargins(0, 1, 0, 1)
		rowAGBHeaderChecksum.addWidget(lblAGBHeaderChecksum)
		self.lblAGBHeaderChecksumResult = QtWidgets.QLabel("")
		rowAGBHeaderChecksum.addWidget(self.lblAGBHeaderChecksumResult)
		group_layout.addLayout(rowAGBHeaderChecksum)

		rowAGBHeaderROMChecksum = QtWidgets.QHBoxLayout()
		lblAGBHeaderROMChecksum = QtWidgets.QLabel("ROM Checksum:")
		lblAGBHeaderROMChecksum.setContentsMargins(0, 1, 0, 1)
		rowAGBHeaderROMChecksum.addWidget(lblAGBHeaderROMChecksum)
		self.lblAGBHeaderROMChecksumResult = QtWidgets.QLabel("")
		rowAGBHeaderROMChecksum.addWidget(self.lblAGBHeaderROMChecksumResult)
		group_layout.addLayout(rowAGBHeaderROMChecksum)
		
		rowAGBHeaderROMSize = QtWidgets.QHBoxLayout()
		lblAGBHeaderROMSize = QtWidgets.QLabel("ROM Size:")
		rowAGBHeaderROMSize.addWidget(lblAGBHeaderROMSize)
		self.cmbAGBHeaderROMSizeResult = QtWidgets.QComboBox()
		self.cmbAGBHeaderROMSizeResult.setStyleSheet("combobox-popup: 0;");
		self.cmbAGBHeaderROMSizeResult.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.cmbAGBHeaderROMSizeResult.addItems(self.AGB_Header_ROM_Sizes)
		self.cmbAGBHeaderROMSizeResult.setCurrentIndex(self.cmbAGBHeaderROMSizeResult.count() - 1)
		rowAGBHeaderROMSize.addWidget(self.cmbAGBHeaderROMSizeResult)
		group_layout.addLayout(rowAGBHeaderROMSize)
		
		rowAGBHeaderRAMSize = QtWidgets.QHBoxLayout()
		lblAGBHeaderRAMSize = QtWidgets.QLabel("Save Type:")
		rowAGBHeaderRAMSize.addWidget(lblAGBHeaderRAMSize)
		self.cmbAGBSaveTypeResult = QtWidgets.QComboBox()
		self.cmbAGBSaveTypeResult.setStyleSheet("combobox-popup: 0;");
		self.cmbAGBSaveTypeResult.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.cmbAGBSaveTypeResult.addItems(self.AGB_Header_Save_Types)
		self.cmbAGBSaveTypeResult.setCurrentIndex(self.cmbAGBSaveTypeResult.count() - 1)
		rowAGBHeaderRAMSize.addWidget(self.cmbAGBSaveTypeResult)
		group_layout.addLayout(rowAGBHeaderRAMSize)
		
		rowAGBCartridgeType = QtWidgets.QHBoxLayout()
		lblAGBCartridgeType = QtWidgets.QLabel("Type:")
		rowAGBCartridgeType.addWidget(lblAGBCartridgeType)
		self.cmbAGBCartridgeTypeResult = QtWidgets.QComboBox()
		self.cmbAGBCartridgeTypeResult.setStyleSheet("max-width: 260px;")
		self.cmbAGBCartridgeTypeResult.setStyleSheet("combobox-popup: 0;");
		self.cmbAGBCartridgeTypeResult.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.cmbAGBCartridgeTypeResult.currentIndexChanged.connect(self.CartridgeTypeChanged)
		rowAGBCartridgeType.addWidget(self.cmbAGBCartridgeTypeResult)
		group_layout.addLayout(rowAGBCartridgeType)

		self.grpAGBCartridgeInfo.setLayout(group_layout)
		return self.grpAGBCartridgeInfo
	
	def UpdateCheck(self):
		update_check = self.SETTINGS.value("UpdateCheck")
		if update_check is None:
			answer = QtWidgets.QMessageBox.question(self, "{:s} {:s}".format(APPNAME, VERSION), "Welcome to {:s} {:s} by Lesserkuma!\nWould you like to automatically check for new versions at application startup?".format(APPNAME, VERSION), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
			if answer == QtWidgets.QMessageBox.Yes:
				self.SETTINGS.setValue("UpdateCheck", "enabled")
				self.mnuConfig.actions()[0].setChecked(True)
				update_check = "enabled"
			else:
				self.SETTINGS.setValue("UpdateCheck", "disabled")
		
		if update_check and update_check.lower() == "enabled":
			if ".dev" in VERSION_PEP440:
				type = "test "
				url = "https://test.pypi.org/pypi/FlashGBX/json"
				site = "https://test.pypi.org/project/FlashGBX/"
			else:
				type = ""
				url = "https://pypi.org/pypi/FlashGBX/json"
				site = "https://github.com/lesserkuma/FlashGBX"
			try:
				ret = requests.get(url, allow_redirects=True, timeout=1.5)
			except requests.exceptions.ConnectTimeout as e:
				print("ERROR: Update check failed due to a connection timeout. Please check your internet connection.", e, sep="\n")
				ret = False
			except requests.exceptions.ConnectionError as e:
				print("ERROR: Update check failed due to a connection error. Please check your network connection.", e, sep="\n")
				ret = False
			except Exception as e:
				print("ERROR: An unexpected error occured while querying the latest version information from PyPI.", e, sep="\n")
				ret = False
			
			if ret is not False and ret.status_code == 200:
				ret = ret.content
				try:
					ret = json.loads(ret)
					if 'info' in ret and 'version' in ret['info']:
						if pkg_resources.parse_version(ret['info']['version']) == pkg_resources.parse_version(VERSION_PEP440):
							print("You are using the latest {:s}version of {:s}.".format(type, APPNAME))
						elif pkg_resources.parse_version(ret['info']['version']) > pkg_resources.parse_version(VERSION_PEP440):
							msg_text = "A new {:s}version of {:s} has been released!\nVersion {:s} is now available.".format(type, APPNAME, ret['info']['version'])
							print(msg_text)
							msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Question, windowTitle="{:s} Update Check".format(APPNAME), text=msg_text)
							button_open = msgbox.addButton("  Open &website  ", QtWidgets.QMessageBox.ActionRole)
							button_cancel = msgbox.addButton("&OK", QtWidgets.QMessageBox.RejectRole)
							msgbox.setDefaultButton(button_open)
							msgbox.setEscapeButton(button_cancel)
							answer = msgbox.exec()
							if msgbox.clickedButton() == button_open:
								webbrowser.open(site)
						else:
							print("This version of {:s} ({:s}) seems to be newer than the latest {:s}release ({:s}). Please check for updates manually.".format(APPNAME, VERSION_PEP440, type, ret['info']['version']))
					else:
						print("ERROR: Update check failed due to missing version information in JSON data from PyPI.")
				except json.decoder.JSONDecodeError:
					print("ERROR: Update check failed due to malformed JSON data from PyPI.")
				except Exception as e:
					print("ERROR: An unexpected error occured while querying the latest version information from PyPI.", e, sep="\n")
			elif ret is not False:
				print("ERROR: Failed to check for updates (HTTP status {:d}).".format(ret.status_code))
	
	def DisconnectDevice(self):
		try:
			devname = self.CONN.GetFullName()
			self.CONN.Close()
			print("Disconnected from {:s}".format(devname))
		except:
			pass
		
		self.CONN = None
		#self.btnScan.show()
		self.optAGB.setEnabled(False)
		self.optDMG.setEnabled(False)
		self.grpDMGCartridgeInfo.setEnabled(False)
		self.grpAGBCartridgeInfo.setEnabled(False)
		self.btnCancel.setEnabled(False)
		self.btnHeaderRefresh.setEnabled(False)
		self.btnBackupROM.setEnabled(False)
		self.btnFlashROM.setEnabled(False)
		self.btnBackupRAM.setEnabled(False)
		self.btnRestoreRAM.setEnabled(False)
		self.btnConnect.setText("Connect")
		self.lblDevice.setText("Disconnected.")
	
	def OpenConfigDir(self):
		path = 'file://{0:s}'.format(self.CONFIG_PATH)
		try:
			if platform.system() == "Windows":
				os.startfile(path)
			elif platform.system() == "Darwin":
				subprocess.Popen(["open", path])
			else:
				subprocess.Popen(["xdg-open", path])
		except:
			QtWidgets.QMessageBox.information(self, "{:s} {:s}".format(APPNAME, VERSION), "Your configuration files are stored in\n" + path, QtWidgets.QMessageBox.Ok)
	
	def ConnectDevice(self):
		if self.CONN is not None:
			self.DisconnectDevice()
			return True
		else:
			if self.cmbDevice.count() > 0:
				index = self.cmbDevice.currentText()
			else:
				index = self.lblDevice.text()

			if index not in self.DEVICES:
				self.FindDevices(True)
				return
			
			dev = self.DEVICES[index]
			ret = dev.Initialize(self.FLASHCARTS)
			msg = ""
			
			if ret is False:
				self.CONN = None
				if self.cmbDevice.count() == 0: self.lblDevice.setText("No connection.")
				return False
			
			elif isinstance(ret, list):
				for i in range(0, len(ret)):
					status = ret[i][0]
					text = ret[i][1]
					if status == 0:
						msg += text + "\n"
					elif status == 1:
						msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Information, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text=text, standardButtons=QtWidgets.QMessageBox.Ok)
						if not '\n' in text: msgbox.setTextFormat(QtCore.Qt.RichText)
						msgbox.exec()
					elif status == 2:
						msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Warning, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text=text, standardButtons=QtWidgets.QMessageBox.Ok)
						if not '\n' in text: msgbox.setTextFormat(QtCore.Qt.RichText)
						msgbox.exec()
					elif status == 3:
						msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Critical, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text=text, standardButtons=QtWidgets.QMessageBox.Ok)
						if not '\n' in text: msgbox.setTextFormat(QtCore.Qt.RichText)
						msgbox.exec()
						self.CONN = None
						return False
			
			if dev.IsConnected():
				qt_app.processEvents()
				self.CONN = dev
				#self.btnScan.hide()
				self.optDMG.setAutoExclusive(False)
				self.optAGB.setAutoExclusive(False)
				if "DMG" in self.CONN.GetSupprtedModes():
					self.optDMG.setEnabled(True)
					self.optDMG.setChecked(False)
				if "AGB" in self.CONN.GetSupprtedModes():
					self.optAGB.setEnabled(True)
					self.optAGB.setChecked(False)
				self.optAGB.setAutoExclusive(True)
				self.optDMG.setAutoExclusive(True)
				self.btnConnect.setText("&Disconnect")
				self.cmbDevice.setStyleSheet("QComboBox { border: 0; margin: 0; padding: 0; max-width: 0px; }");
				self.lblDevice.setText(dev.GetFullName())
				print("\nConnected to " + dev.GetFullName())
				self.grpDMGCartridgeInfo.setEnabled(True)
				self.grpAGBCartridgeInfo.setEnabled(True)
				self.grpActions.setEnabled(True)
				self.btnCancel.setEnabled(False)
				self.SetProgressBars(min=0, max=1, value=0)
				
				if self.CONN.GetMode() == "DMG":
					self.cmbDMGCartridgeTypeResult.clear()
					self.cmbDMGCartridgeTypeResult.addItems(self.CONN.GetSupportedCartridgesDMG()[0])
					self.grpAGBCartridgeInfo.setVisible(False)
					self.grpDMGCartridgeInfo.setVisible(True)
				elif self.CONN.GetMode() == "AGB":
					self.cmbAGBCartridgeTypeResult.clear()
					self.cmbAGBCartridgeTypeResult.addItems(self.CONN.GetSupportedCartridgesAGB()[0])
					self.grpDMGCartridgeInfo.setVisible(False)
					self.grpAGBCartridgeInfo.setVisible(True)
				
				print(msg, end="")
				return True
			return False
	
	def FindDevices(self, connectToFirst=False):
		if self.CONN is not None:
			self.DisconnectDevice()
		self.lblDevice.setText("Searching...")
		#self.btnScan.setEnabled(False)
		self.btnConnect.setEnabled(False)
		qt_app.processEvents()
		time.sleep(0.05)
		
		global hw_devices
		for hw_device in hw_devices:
			dev = hw_device.GbxDevice()
			ret = dev.Initialize(self.FLASHCARTS)
			if ret is False:
				self.CONN = None
			elif isinstance(ret, list):
				for i in range(0, len(ret)):
					status = ret[i][0]
					msg = ret[i][1]
					if status == 3:
						QtWidgets.QMessageBox.critical(self, "{:s} {:s}".format(APPNAME, VERSION), msg, QtWidgets.QMessageBox.Ok)
						self.CONN = None
			
			if dev.IsConnected():
				self.DEVICES[dev.GetFullName()] = dev
				dev.Close()
		
		self.cmbDevice.setStyleSheet("QComboBox { border: 0; margin: 0; padding: 0; max-width: 0px; }");
		
		if len(self.DEVICES) == 0:
			self.lblDevice.setText("No devices found.")
			self.lblDevice.setStyleSheet("");
			self.cmbDevice.clear()
			self.btnConnect.setEnabled(False)
		elif len(self.DEVICES) == 1 or (connectToFirst and len(self.DEVICES) > 1):
			self.lblDevice.setText(list(self.DEVICES.keys())[0])
			self.lblDevice.setStyleSheet("");
			self.ConnectDevice()
			self.cmbDevice.clear()
			self.btnConnect.setEnabled(True)
		else:
			self.lblDevice.setText("Select device:")
			self.cmbDevice.clear()
			self.cmbDevice.addItems(self.DEVICES.keys())
			self.cmbDevice.setCurrentIndex(0)
			self.cmbDevice.setStyleSheet("");
			self.btnConnect.setEnabled(True)
		
		#self.btnScan.setEnabled(True)
		self.btnConnect.setEnabled(True)
		
		if len(self.DEVICES) == 0: return False
		return True

	def AbortOperation(self):
		self.CONN.CANCEL = True

	def FinishOperation(self):
		if self.lblStatus2aResult.text() == "Pending...": self.lblStatus2aResult.setText("–")
		self.lblStatus4aResult.setText("")
		self.grpDMGCartridgeInfo.setEnabled(True)
		self.grpAGBCartridgeInfo.setEnabled(True)
		self.grpActions.setEnabled(True)
		self.btnCancel.setEnabled(False)
		
		dontShowAgain = str(self.SETTINGS.value("SkipFinishMessage")).lower() == "enabled"
		
		msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Information, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="Operation complete!", standardButtons=QtWidgets.QMessageBox.Ok)
		cb = QtWidgets.QCheckBox("Don’t show this message again.", checked=False)
		msgbox.setCheckBox(cb)
		
		if self.CONN.INFO["last_action"] == 4: # Flash ROM
			self.CONN.INFO["last_action"] = 0
			self.ReadCartridge(resetStatus=False)
			self.lblStatus4a.setText("Done!")
			if "verified" in self.PROGRESS and self.PROGRESS["verified"] == True:
				msgbox.setText("The ROM was flashed and verified successfully!")
			else:
				msgbox.setText("ROM flashing complete!")
			if not dontShowAgain:
				msgbox.exec()
				dontShowAgain = cb.isChecked()

		elif self.CONN.INFO["last_action"] == 1: # Backup ROM
			self.CONN.INFO["last_action"] = 0
			
			if self.CONN.GetMode() == "DMG":
				if self.CONN.INFO["rom_checksum"] == self.CONN.INFO["rom_checksum_calc"]:
					self.lblHeaderROMChecksumResult.setText("Valid (0x{:04X})".format(self.CONN.INFO["rom_checksum"]))
					self.lblHeaderROMChecksumResult.setStyleSheet("QLabel { color: green; }");
					self.lblStatus4a.setText("Done!")
					#msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Information, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="The ROM was dumped successfully!", standardButtons=QtWidgets.QMessageBox.Ok)
					msgbox.setText("The ROM backup is complete and the checksum was verified successfully!")
					if not dontShowAgain:
						msgbox.exec()
						dontShowAgain = cb.isChecked()
				else:
					self.lblHeaderROMChecksumResult.setText("Invalid (0x{:04X}≠0x{:04X})".format(self.CONN.INFO["rom_checksum_calc"], self.CONN.INFO["rom_checksum"]))
					self.lblHeaderROMChecksumResult.setStyleSheet("QLabel { color: red; }");
					self.lblStatus4a.setText("Done.")
					QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "The ROM was dumped, but the checksum is not correct. This may indicate a bad dump, however this can be normal for some reproduction cartridges, prototypes and patched games.\nWhen dumping from a flash cartridge, manually selecting MBC5 before dumping may also help.", QtWidgets.QMessageBox.Ok)
			elif self.CONN.GetMode() == "AGB":
				if self.AGB_Global_CRC32 == self.CONN.INFO["rom_checksum_calc"]:
					self.lblAGBHeaderROMChecksumResult.setText("Valid (0x{:06X})".format(self.AGB_Global_CRC32))
					self.lblAGBHeaderROMChecksumResult.setStyleSheet("QLabel { color: green; }");
					self.lblStatus4a.setText("Done!")
					msgbox.setText("The ROM backup is complete and the checksum was verified successfully!")
					if not dontShowAgain:
						msgbox.exec()
						dontShowAgain = cb.isChecked()

				elif self.AGB_Global_CRC32 == 0:
					self.lblAGBHeaderROMChecksumResult.setText("0x{:06X}".format(self.CONN.INFO["rom_checksum_calc"]))
					self.lblAGBHeaderROMChecksumResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
					self.lblStatus4a.setText("Done!")
					QtWidgets.QMessageBox.information(self, "{:s} {:s}".format(APPNAME, VERSION), "The ROM backup is complete!", QtWidgets.QMessageBox.Ok)
				else:
					self.lblAGBHeaderROMChecksumResult.setText("Invalid (0x{:06X}≠0x{:06X})".format(self.CONN.INFO["rom_checksum_calc"], self.AGB_Global_CRC32))
					self.lblAGBHeaderROMChecksumResult.setStyleSheet("QLabel { color: red; }");
					self.lblStatus4a.setText("Done.")
					QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "The ROM backup is complete, but the checksum doesn’t match the known database entry. This may indicate a bad dump, however this can be normal for some reproduction cartridges, prototypes and patched games.", QtWidgets.QMessageBox.Ok)
		
		elif self.CONN.INFO["last_action"] == 2: # Backup RAM
			self.lblStatus4a.setText("Done!")
			self.CONN.INFO["last_action"] = 0
			if self.CONN.INFO["transferred"] == 131072: # 128 KB
				with open(self.CONN.INFO["last_path"], "rb") as file: temp = file.read()
				if temp[0x1FFB1:0x1FFB6] == b'Magic':
					answer = QtWidgets.QMessageBox.question(self, "{:s} {:s}".format(APPNAME, VERSION), "Game Boy Camera save data was detected.\nWould you like to load it with the GB Camera Viewer now?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
					if answer == QtWidgets.QMessageBox.Yes:
						self.CAMWIN = None
						self.CAMWIN = PocketCameraWindow(self, icon=self.windowIcon(), file=self.CONN.INFO["last_path"])
						self.CAMWIN.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
						self.CAMWIN.setModal(True)
						self.CAMWIN.run()
						return
			
			msgbox.setText("The save data backup is complete!")
			if not dontShowAgain:
				msgbox.exec()
				dontShowAgain = cb.isChecked()
		
		elif self.CONN.INFO["last_action"] == 3: # Restore RAM
			self.lblStatus4a.setText("Done!")
			self.CONN.INFO["last_action"] = 0
			if "save_erase" in self.CONN.INFO and self.CONN.INFO["save_erase"]:
				msg_text = "The save data was erased."
				del(self.CONN.INFO["save_erase"])
			else:
				msg_text = "The save data was restored!"
			msgbox.setText(msg_text)
			if not dontShowAgain:
				msgbox.exec()
				dontShowAgain = cb.isChecked()
		
		else:
			self.lblStatus4a.setText("Ready.")
			self.CONN.INFO["last_action"] = 0
		
		if dontShowAgain: self.SETTINGS.setValue("SkipFinishMessage", "enabled")
		self.SetProgressBars(min=0, max=1, value=1)
	
	def CartridgeTypeAutoDetect(self):
		cart_type = 0
		cart_text = ""
		
		if self.CONN.CheckROMStable() is False:
			QtWidgets.QMessageBox.critical(self, "{:s} {:s}".format(APPNAME, VERSION), "Unstable ROM reading detected. Please make sure you selected the correct mode and that the cartridge contacts are clean.", QtWidgets.QMessageBox.Ok)
			return 0
		
		if self.CONN.GetMode() in self.FLASHCARTS and len(self.FLASHCARTS[self.CONN.GetMode()]) == 0:
			QtWidgets.QMessageBox.critical(self, "{:s} {:s}".format(APPNAME, VERSION), "No flash cartridge type configuration files found. Try to restart the application with the “--reset” switch to reset the configuration.", QtWidgets.QMessageBox.Ok)
			return 0
		
		msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Question, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="Would you like " + APPNAME + " to try and auto-detect the flash cartridge type?\n(Official game cartridges can not be re-written.)", standardButtons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, defaultButton=QtWidgets.QMessageBox.Yes)
		cb = QtWidgets.QCheckBox("Limit voltage to 3.3V", checked=True)
		if self.CONN.GetMode() == "DMG":
			msgbox.setCheckBox(cb)
		answer = msgbox.exec()
		limitVoltage = cb.isChecked()
		if answer == QtWidgets.QMessageBox.No:
			return 0
		else:
			detected = self.CONN.AutoDetectFlash(limitVoltage)
			if len(detected) == 0:
				msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Question, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="No pre-configured flash cartridge type was detected. You can still try and manually select one from the list -- look for similar PCB text and/or flash chip markings. However, chances are this cartridge is currently not supported for flashing with " + APPNAME + ".\n\nWould you like " + APPNAME + " to run a flash chip query? This may help adding support for your flash cartridge in the future.", standardButtons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, defaultButton=QtWidgets.QMessageBox.Yes)
				if self.CONN.GetMode() == "DMG":
					msgbox.setCheckBox(cb)
				answer = msgbox.exec()
				if self.CONN.GetMode() == "DMG":
					limitVoltage = cb.isChecked()
				else:
					limitVoltage = False
				
				if answer == QtWidgets.QMessageBox.Yes:
					(flash_id, cfi_s, cfi) = self.CONN.CheckFlashChip(limitVoltage)
					if cfi_s == "":
						QtWidgets.QMessageBox.information(self, "{:s} {:s}".format(APPNAME, VERSION), "Flash chip query result: <pre>" + flash_id + "</pre>There was no Common Flash Interface (CFI) response from the cartridge. If a flash chip exists on the cartridge PCB, it may be too old or require unique unlocking and handling.", QtWidgets.QMessageBox.Ok)
					else:
						QtWidgets.QMessageBox.information(self, "{:s} {:s}".format(APPNAME, VERSION), "Flash chip query result: <pre>" + flash_id + "</pre><pre>" + str(cfi_s) + "</pre>", QtWidgets.QMessageBox.Ok)
						with open(self.CONFIG_PATH + "/cfi.bin", "wb") as f: f.write(cfi['raw'])
				return 0
			else:
				cart_type = detected[0]
				size_undetected = False
				if self.CONN.GetMode() == "DMG":
					cart_types = self.CONN.GetSupportedCartridgesDMG()
					size = cart_types[1][detected[0]]["flash_size"]
					for i in range(0, len(detected)):
						if size != cart_types[1][detected[i]]["flash_size"]:
							size_undetected = True
						cart_text += "- " + cart_types[0][detected[i]] + "\n"
				elif self.CONN.GetMode() == "AGB":
					cart_types = self.CONN.GetSupportedCartridgesAGB()
					size = cart_types[1][detected[0]]["flash_size"]
					for i in range(0, len(detected)):
						if size != cart_types[1][detected[i]]["flash_size"]:
							size_undetected = True
						cart_text += "- " + cart_types[0][detected[i]] + "\n"
				
				if size_undetected:
					(flashid, cfi_s, cfi) = self.CONN.CheckFlashChip(limitVoltage=limitVoltage, cart_type=cart_types[1][cart_type])
					if isinstance(cfi, dict) and 'device_size' in cfi:
						for i in range(0, len(detected)):
							if cfi['device_size'] == cart_types[1][detected[i]]["flash_size"]:
								cart_type = detected[i]
								size_undetected = False
								break
				
				if len(detected) == 1:
					msg_text = "The following flash cartridge type was detected:\n" + cart_text + "\nThe supported ROM size is up to {:d} MB unless specified otherwise.".format(int(cart_types[1][cart_type]['flash_size'] / 1024 / 1024))
				else:
					if size_undetected is True:
						msg_text = "The following flash cartridge type variants were detected:\n" + cart_text + "\nThe first one will now be auto-selected, but you might need to adjust the selection.\n\nIMPORTANT: While these cartridges share the same electronic signature, their supported ROM size can differ. As the size can not be detected automatically at this time, please select it manually."
					else:
						msg_text = "The following flash cartridge type variants were detected:\n" + cart_text + "\nAll from this list should work the same. The first name/alias will now be auto-selected.\n\nThe supported ROM size is up to {:d} MB.".format(int(cart_types[1][cart_type]['flash_size'] / 1024 / 1024))
				
				msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Question, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text=msg_text)
				button_ok = msgbox.addButton("&OK", QtWidgets.QMessageBox.ActionRole)
				button_cancel = msgbox.addButton("&Cancel", QtWidgets.QMessageBox.RejectRole)
				button_cfi = msgbox.addButton("  Run flash chip &query  ", QtWidgets.QMessageBox.ActionRole)
				msgbox.setDefaultButton(button_ok)
				msgbox.setEscapeButton(button_cancel)
				answer = msgbox.exec()
				if msgbox.clickedButton() == button_cfi:
					(flash_id, cfi_s, cfi) = self.CONN.CheckFlashChip(limitVoltage=limitVoltage, cart_type=cart_types[1][cart_type])
					if cfi_s == "":
						QtWidgets.QMessageBox.information(self, "{:s} {:s}".format(APPNAME, VERSION), "Flash chip query result: <pre>" + flash_id + "</pre>There was no Common Flash Interface (CFI) response from the cartridge. If a flash chip exists on the cartridge PCB, it may be too old or require unique unlocking and handling.", QtWidgets.QMessageBox.Ok)
					else:
						QtWidgets.QMessageBox.information(self, "{:s} {:s}".format(APPNAME, VERSION), "Flash chip query result: <pre>" + flash_id + "</pre><pre>" + str(cfi_s) + "</pre>", QtWidgets.QMessageBox.Ok)
						with open(self.CONFIG_PATH + "/cfi.bin", "wb") as f: f.write(cfi['raw'])
				elif msgbox.clickedButton() == button_cancel: return 0
		
		return cart_type
	
	def CartridgeTypeChanged(self, index):
		if self.CONN.GetMode() == "DMG":
			cart_types = self.CONN.GetSupportedCartridgesDMG()
			if cart_types[1][index] == "AUTODETECT": # special keyword
				cart_type = self.CartridgeTypeAutoDetect()
				if (cart_type == 1): cart_type = 0
				self.cmbDMGCartridgeTypeResult.setCurrentIndex(cart_type)
			elif cart_types[1][index] == "RETAIL": # special keyword
				pass
			else:
				for i in range(0, len(self.DMG_Header_ROM_Sizes_Flasher_Map)):
					if cart_types[1][index]["flash_size"] == (self.DMG_Header_ROM_Sizes_Flasher_Map[i] * 0x4000):
						self.cmbHeaderROMSizeResult.setCurrentIndex(i)
		
		elif self.CONN.GetMode() == "AGB":
			cart_types = self.CONN.GetSupportedCartridgesAGB()
			if cart_types[1][index] == "AUTODETECT": # special keyword
				cart_type = self.CartridgeTypeAutoDetect()
				if (cart_type == 1): cart_type = 0
				self.cmbAGBCartridgeTypeResult.setCurrentIndex(cart_type)
			elif cart_types[1][index] == "RETAIL": # special keyword
				pass
			else:
				self.cmbAGBHeaderROMSizeResult.setCurrentIndex(self.AGB_Header_ROM_Sizes_Map.index(cart_types[1][index]["flash_size"]))
	
	def BackupROM(self):
		if not self.CheckDeviceAlive(): return
		mbc = self.DMG_Header_Features_MBC[self.cmbHeaderFeaturesResult.currentIndex()]
		rom_banks = self.DMG_Header_ROM_Sizes_Flasher_Map[self.cmbHeaderROMSizeResult.currentIndex()]
		
		fast_read_mode = self.SETTINGS.value("FastReadMode")
		if fast_read_mode and fast_read_mode.lower() == "enabled":
			fast_read_mode = True
		else:
			fast_read_mode = False
		
		rom_size = 0
		if self.CONN.GetMode() == "DMG":
			if mbc == 1 and ("MOMOCOL" in self.lblHeaderTitleResult.text() or "BOMCOL" in self.lblHeaderTitleResult.text()):
				mbc = 1.1
			setting_name = "LastDirRomDMG"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			path = self.lblHeaderTitleResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			if path == "": path = "ROM"
			path = re.sub(r"[<>:\"/\\|\?\*]", "_", path)
			if self.CONN.INFO["cgb"] == 0xC0 or self.CONN.INFO["cgb"] == 0x80:
				path = path + ".gbc"
			elif self.CONN.INFO["sgb"] == 0x03:
				path = path + ".sgb"
			else:
				path = path + ".gb"
			path = QtWidgets.QFileDialog.getSaveFileName(self, "Backup ROM", last_dir + "/" + path, "Game Boy ROM File (*.gb *.sgb *.gbc);;All Files (*.*)")[0]
		
		elif self.CONN.GetMode() == "AGB":
			setting_name = "LastDirRomAGB"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			path = self.lblAGBHeaderTitleResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			if path == "": path = self.lblAGBHeaderCodeResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			if path == "": path = "ROM"
			path = re.sub(r"[<>:\"/\\|\?\*]", "_", path)
			rom_size = self.AGB_Header_ROM_Sizes_Map[self.cmbAGBHeaderROMSizeResult.currentIndex()]
			path = path + ".gba"
			path = QtWidgets.QFileDialog.getSaveFileName(self, "Backup ROM", last_dir + "/" + path, "Game Boy Advance ROM File (*.gba *.srl);;All Files (*.*)")[0]
		
		if (path == ""): return
		
		self.SETTINGS.setValue(setting_name, os.path.dirname(path))
		self.lblHeaderROMChecksumResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
		self.lblAGBHeaderROMChecksumResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
		
		self.CONN.BackupROM(fncSetProgress=self.SetProgress, path=path, mbc=mbc, rom_banks=rom_banks, agb_rom_size=rom_size, fast_read_mode=fast_read_mode)

	def FlashROM(self, dpath=""):
		if not self.CheckDeviceAlive(): return
		path = ""
		if dpath != "":
			#text = "The following ROM file will now be written to the flash cartridge:\n" + dpath
			#answer = QtWidgets.QMessageBox.question(self, "{:s} {:s}".format(APPNAME, VERSION), text, QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Ok)
			#if answer == QtWidgets.QMessageBox.Cancel: return
			path = dpath
		
		if self.CONN.GetMode() == "DMG":
			setting_name = "LastDirRomDMG"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			carts = self.CONN.GetSupportedCartridgesDMG()[1]
			cart_type = self.cmbDMGCartridgeTypeResult.currentIndex()
		elif self.CONN.GetMode() == "AGB":
			setting_name = "LastDirRomAGB"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			carts = self.CONN.GetSupportedCartridgesAGB()[1]
			cart_type = self.cmbAGBCartridgeTypeResult.currentIndex()
		else:
			return
		
		if cart_type == 0:
			cart_type = self.CartridgeTypeAutoDetect()
			if (cart_type == 1): cart_type = 0
			if self.CONN.GetMode() == "DMG":
				self.cmbDMGCartridgeTypeResult.setCurrentIndex(cart_type)
			elif self.CONN.GetMode() == "AGB":
				self.cmbAGBCartridgeTypeResult.setCurrentIndex(cart_type)
			if cart_type == 0: return
		
		while path == "":
			if self.CONN.GetMode() == "DMG":
				path = QtWidgets.QFileDialog.getOpenFileName(self, "Flash ROM", last_dir, "Game Boy ROM File (*.gb *.gbc *.sgb *.bin);;All Files (*.*)")[0]
			elif self.CONN.GetMode() == "AGB":
				path = QtWidgets.QFileDialog.getOpenFileName(self, "Flash ROM", last_dir, "Game Boy Advance ROM File (*.gba *.srl);;All Files (*.*)")[0]
			
			if (path == ""): return
		
		self.SETTINGS.setValue(setting_name, os.path.dirname(path))
		
		if os.path.getsize(path) > 0x2000000: # reject too large files to avoid exploding RAM
			QtWidgets.QMessageBox.critical(self, "{:s} {:s}".format(APPNAME, VERSION), "Files bigger than 32 MB are not supported.", QtWidgets.QMessageBox.Ok)
			return
		
		with open(path, "rb") as file: buffer = file.read()
		rom_size = len(buffer)
		if rom_size > carts[cart_type]['flash_size']:
			answer = QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "The selected flash cartridge type seems to support ROMs that are up to " + str(int(carts[cart_type]['flash_size'] / 1024 / 1024)) + " MB in size, but the file you selected is " + str(os.path.getsize(path)/1024/1024) + " MB. You can still give it a try, but it’s possible that it’s too large.", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
			if answer == QtWidgets.QMessageBox.Cancel: return
		
		override_voltage = False
		if 'voltage_variants' in carts[cart_type] and carts[cart_type]['voltage'] == 3.3:
			msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Question, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="The selected flash cartridge type usually flashes fine with 3.3V, however sometimes it may require 5V. Which mode should be used?")
			button_3_3v = msgbox.addButton("  Use &3.3V (safer)  ", QtWidgets.QMessageBox.ActionRole)
			button_5v = msgbox.addButton("Use &5V", QtWidgets.QMessageBox.ActionRole)
			button_cancel = msgbox.addButton("&Cancel", QtWidgets.QMessageBox.RejectRole)
			msgbox.setDefaultButton(button_3_3v)
			msgbox.setEscapeButton(button_cancel)
			answer = msgbox.exec()
			if msgbox.clickedButton() == button_5v:
				override_voltage = 5
			elif msgbox.clickedButton() == button_cancel: return
		
		reverse_sectors = False
		if 'sector_reversal' in carts[cart_type]:
			msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Question, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="The selected flash cartridge type is reported to sometimes have reversed sectors. If the cartridge is not working after flashing, try reversed sectors.")
			button_normal = msgbox.addButton("Normal", QtWidgets.QMessageBox.ActionRole)
			button_reversed = msgbox.addButton("Reversed", QtWidgets.QMessageBox.ActionRole)
			button_cancel = msgbox.addButton("&Cancel", QtWidgets.QMessageBox.RejectRole)
			msgbox.setDefaultButton(button_normal)
			msgbox.setEscapeButton(button_cancel)
			answer = msgbox.exec()
			if msgbox.clickedButton() == button_reversed:
				reverse_sectors = True
			elif msgbox.clickedButton() == button_cancel: return
		
		prefer_sector_erase = False
		if 'chip_erase' in carts[cart_type]['commands'] and 'sector_erase' in carts[cart_type]['commands']:
			prefer_sector_erase = self.SETTINGS.value("PreferSectorErase")
			if prefer_sector_erase and prefer_sector_erase.lower() == "enabled":
				prefer_sector_erase = True
			else:
				prefer_sector_erase = False

		fast_read_mode = self.SETTINGS.value("FastReadMode")
		if fast_read_mode and fast_read_mode.lower() == "enabled":
			fast_read_mode = True
		else:
			fast_read_mode = False
		
		verify_flash = self.SETTINGS.value("VerifyFlash")
		if verify_flash and verify_flash.lower() == "enabled":
			verify_flash = True
		else:
			verify_flash = False
		
		try:
			if self.CONN.GetMode() == "DMG":
				hdr = RomFileDMG(path).GetHeader()
			elif self.CONN.GetMode() == "AGB":
				hdr = RomFileAGB(path).GetHeader()
			if not hdr["logo_correct"]:
				answer = QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "Warning: The ROM file you selected will not boot on actual hardware due to invalid logo data.", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
				if answer == QtWidgets.QMessageBox.Cancel: return
			if not hdr["header_checksum_correct"]:
				answer = QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "Warning: The ROM file you selected will not boot on actual hardware due to an invalid header checksum (expected 0x{:02X} instead of 0x{:02X}).".format(hdr["header_checksum_calc"], hdr["header_checksum"]), QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
				if answer == QtWidgets.QMessageBox.Cancel: return
		except:
			QtWidgets.QMessageBox.critical(self, "{:s} {:s}".format(APPNAME, VERSION), "The file you selected could not be read.", QtWidgets.QMessageBox.Ok)
			return
		
		self.CONN.FlashROM(fncSetProgress=self.SetProgress, path=path, cart_type=cart_type, override_voltage=override_voltage, prefer_sector_erase=prefer_sector_erase, reverse_sectors=reverse_sectors, fast_read_mode=fast_read_mode, verify_flash=verify_flash)
		buffer = None
	
	def BackupRAM(self):
		if not self.CheckDeviceAlive(): return
		if self.CONN.GetMode() == "DMG":
			setting_name = "LastDirSaveDataDMG"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			path = self.lblHeaderTitleResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			if path == "": path = "ROM"
			features = self.DMG_Header_Features_MBC[self.cmbHeaderFeaturesResult.currentIndex()]
			save_type = self.DMG_Header_RAM_Sizes_Flasher_Map[self.cmbHeaderRAMSizeResult.currentIndex()]
			if save_type == 0:
				QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "Please select the correct save data size.", QtWidgets.QMessageBox.Ok)
				return
		elif self.CONN.GetMode() == "AGB":
			setting_name = "LastDirSaveDataAGB"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			path = self.lblAGBHeaderTitleResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			if path == "": path = self.lblAGBHeaderCodeResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			if path == "": path = "ROM"
			features = 0
			save_type = self.cmbAGBSaveTypeResult.currentIndex()
			if save_type == 0:
				QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "The save type was not selected or auto-detection failed.", QtWidgets.QMessageBox.Ok)
				return
		else:
			return
		
		add_date_time = self.SETTINGS.value("SaveFileNameAddDateTime")
		if add_date_time and add_date_time.lower() == "enabled":
			path = re.sub(r"[<>:\"/\\|\?\*]", "_", path) + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".sav"
		else:
			path = re.sub(r"[<>:\"/\\|\?\*]", "_", path) + ".sav"
		
		path = QtWidgets.QFileDialog.getSaveFileName(self, "Backup Save Data", last_dir + "/" + path, "Save Data File (*.sav);;All Files (*.*)")[0]
		
		if (path == ""): return
		
		self.SETTINGS.setValue(setting_name, os.path.dirname(path))
		self.CONN.BackupRAM(fncSetProgress=self.SetProgress, path=path, mbc=features, save_type=save_type)

	def WriteRAM(self, dpath="", erase=False):
		if not self.CheckDeviceAlive(): return
		if self.CONN.GetMode() == "DMG":
			setting_name = "LastDirSaveDataDMG"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			if dpath == "": path = self.lblHeaderTitleResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			features = self.DMG_Header_Features_MBC[self.cmbHeaderFeaturesResult.currentIndex()]
			save_type = self.DMG_Header_RAM_Sizes_Flasher_Map[self.cmbHeaderRAMSizeResult.currentIndex()]
			if save_type == 0:
				QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "Please select the correct save data size.", QtWidgets.QMessageBox.Ok)
				return
		elif self.CONN.GetMode() == "AGB":
			setting_name = "LastDirSaveDataAGB"
			last_dir = self.SETTINGS.value(setting_name)
			if last_dir is None: last_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
			if dpath == "": path = self.lblAGBHeaderTitleResult.text().strip().encode('ascii', 'ignore').decode('ascii')
			features = 0
			save_type = self.cmbAGBSaveTypeResult.currentIndex()
			if save_type == 0:
				QtWidgets.QMessageBox.critical(self, "{:s} {:s}".format(APPNAME, VERSION), "The save type was not selected or auto-detection failed.", QtWidgets.QMessageBox.Ok)
				return
		else:
			return
		
		if dpath != "":
			text = "The following save data file will now be written to the cartridge:\n" + dpath
			answer = QtWidgets.QMessageBox.question(self, "{:s} {:s}".format(APPNAME, VERSION), text, QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Ok)
			if answer == QtWidgets.QMessageBox.Cancel: return
			path = dpath
			self.SETTINGS.setValue(setting_name, os.path.dirname(path))
		elif erase:
			answer = QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "The save data on your cartridge will now be erased.", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
			if answer == QtWidgets.QMessageBox.Cancel: return
		else:
			path = path + ".sav"
			path = QtWidgets.QFileDialog.getOpenFileName(self, "Restore Save Data", last_dir + "/" + path, "Save Data File (*.sav);;All Files (*.*)")[0]
			if not path == "": self.SETTINGS.setValue(setting_name, os.path.dirname(path))
			if (path == ""): return
			if os.path.getsize(path) > 0x100000: # reject too large files to avoid exploding RAM
				QtWidgets.QMessageBox.critical(self, "{:s} {:s}".format(APPNAME, VERSION), "Files bigger than 1 MB are not supported.", QtWidgets.QMessageBox.Ok)
				return
		
		self.CONN.RestoreRAM(fncSetProgress=self.SetProgress, path=path, mbc=features, save_type=save_type, erase=erase)
	
	def CheckDeviceAlive(self, setMode=False):
		if self.CONN is not None:
			mode = self.CONN.GetMode()
			if self.CONN.DEVICE is not None:
				if not self.CONN.IsConnected():
					self.DisconnectDevice()
					self.DEVICES = {}
					dontShowAgain = str(self.SETTINGS.value("AutoReconnect")).lower() == "enabled"
					if not dontShowAgain:
						cb = QtWidgets.QCheckBox("Always try to reconnect without asking", checked=False)
						msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Question, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="The connection to the device was lost. Do you want to try and reconnect to the first device found? The cartridge information will also be reset and read again.", standardButtons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, defaultButton=QtWidgets.QMessageBox.Yes)
						msgbox.setCheckBox(cb)
						answer = msgbox.exec()
						dontShowAgain = cb.isChecked()
						if dontShowAgain: self.SETTINGS.setValue("AutoReconnect", "enabled")
						if answer == QtWidgets.QMessageBox.No:
							return False
					if self.FindDevices(True):
						if setMode is not False: mode = setMode
						if mode == "DMG": self.optDMG.setChecked(True)
						elif mode == "AGB": self.optAGB.setChecked(True)
						self.SetMode()
						return True
					else:
						return False
				else:
					return True
		return False
	
	def SetMode(self):
		setTo = False
		mode = self.CONN.GetMode()
		if mode == "DMG":
			if self.optDMG.isChecked(): return
			setTo = "AGB"
		elif mode == "AGB":
			if self.optAGB.isChecked(): return
			setTo = "DMG"
		else: # mode not set yet
			if self.optDMG.isChecked():
				setTo = "DMG"
			elif self.optAGB.isChecked():
				setTo = "AGB"
		
		voltageWarning = ""
		if self.CONN.CanSetVoltageAutomatically(): # device can switch in software
			dontShowAgain = str(self.SETTINGS.value("SkipModeChangeWarning")).lower() == "enabled"
		elif self.CONN.CanSetVoltageManually(): # device has a physical switch
			voltageWarning = "\n\nImportant: Also make sure your device is set to the correct voltage!"
			dontShowAgain = False
		else: # no voltage switching supported
			dontShowAgain = False
		
		if not dontShowAgain and mode is not None:
			cb = QtWidgets.QCheckBox("Don’t show this message again.", checked=False)
			msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Warning, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text="The mode will now be changed to " + {"DMG":"Game Boy", "AGB":"Game Boy Advance"}[setTo] + " mode. To be safe, cartridges should only be exchanged while the device is not powered on." + voltageWarning, standardButtons=QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, defaultButton=QtWidgets.QMessageBox.Ok)
			if self.CONN.CanSetVoltageAutomatically(): msgbox.setCheckBox(cb)
			answer = msgbox.exec()
			dontShowAgain = cb.isChecked()
			if answer == QtWidgets.QMessageBox.Cancel:
				if mode == "DMG": self.optDMG.setChecked(True)
				if mode == "AGB": self.optAGB.setChecked(True)
				return False
			if dontShowAgain: self.SETTINGS.setValue("SkipModeChangeWarning", "enabled")
		
		if not self.CheckDeviceAlive(setMode=setTo): return
		
		if self.optDMG.isChecked() and (mode == "AGB" or mode == None):
			self.CONN.SetMode("DMG")
		elif self.optAGB.isChecked() and (mode == "DMG" or mode == None):
			self.CONN.SetMode("AGB")
		
		self.ReadCartridge()
		qt_app.processEvents()
		self.btnHeaderRefresh.setEnabled(True)
		self.btnBackupROM.setEnabled(True)
		self.btnFlashROM.setEnabled(True)
		self.btnBackupRAM.setEnabled(True)
		self.btnRestoreRAM.setEnabled(True)
		self.grpDMGCartridgeInfo.setEnabled(True)
		self.grpAGBCartridgeInfo.setEnabled(True)
	
	def ReadCartridge(self, resetStatus=True):
		if not self.CheckDeviceAlive(): return
		data = self.CONN.ReadInfo()
		
		if data == False or len(data) == 0:
			self.DisconnectDevice()
			return False
				
		if self.CONN.GetMode() == "DMG":
			self.cmbDMGCartridgeTypeResult.clear()
			self.cmbDMGCartridgeTypeResult.addItems(self.CONN.GetSupportedCartridgesDMG()[0])
			self.cmbDMGCartridgeTypeResult.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
			if "flash_type" in data:
				self.cmbDMGCartridgeTypeResult.setCurrentIndex(data["flash_type"])
			
			self.lblHeaderTitleResult.setText(data['game_title'])
			if data['sgb'] in self.DMG_Header_SGB:
				self.lblHeaderSGBResult.setText(self.DMG_Header_SGB[data['sgb']])
			else:
				self.lblHeaderSGBResult.setText("Unknown (0x{:02X})".format(data['sgb']))
			if data['cgb'] in self.DMG_Header_CGB:
				self.lblHeaderCGBResult.setText(self.DMG_Header_CGB[data['cgb']])
			else:
				self.lblHeaderCGBResult.setText("Unknown (0x{:02X})".format(data['cgb']))
			if data['logo_correct']:
				self.lblHeaderLogoValidResult.setText("OK")
				self.lblHeaderLogoValidResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
			else:
				self.lblHeaderLogoValidResult.setText("Invalid")
				self.lblHeaderLogoValidResult.setStyleSheet("QLabel { color: red; }");
			if data['header_checksum_correct']:
				self.lblHeaderChecksumResult.setText("Valid (0x{:02X})".format(data['header_checksum']))
				self.lblHeaderChecksumResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
			else:
				self.lblHeaderChecksumResult.setText("Invalid (0x{:02X})".format(data['header_checksum']))
				self.lblHeaderChecksumResult.setStyleSheet("QLabel { color: red; }");
			self.lblHeaderROMChecksumResult.setText("0x{:04X}".format(data['rom_checksum']))
			self.lblHeaderROMChecksumResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
			for i in range(0, len(self.DMG_Header_ROM_Sizes_Map)):
				if data["rom_size_raw"] == self.DMG_Header_ROM_Sizes_Map[i]:
					self.cmbHeaderROMSizeResult.setCurrentIndex(i)
			for i in range(0, len(self.DMG_Header_RAM_Sizes_Map)):
				if data["ram_size_raw"] == self.DMG_Header_RAM_Sizes_Map[i]:
					self.cmbHeaderRAMSizeResult.setCurrentIndex(i)
			i = 0
			for k, v in self.DMG_Header_Features.items():
				if data["features_raw"] == k:
					self.cmbHeaderFeaturesResult.setCurrentIndex(i)
					if k == 0x05 or k == 0x06: self.cmbHeaderRAMSizeResult.setCurrentIndex(1) # MBC2 Save
				i += 1
			
			if data['empty'] == True: # defaults
				self.lblHeaderTitleResult.setText("(No ROM data detected)")
				self.lblHeaderTitleResult.setStyleSheet("QLabel { color: red; }");
				#self.lblHeaderSGBResult.setText("")
				#self.lblHeaderCGBResult.setText("")
				#self.lblHeaderLogoValidResult.setText("")
				#self.lblHeaderChecksumResult.setText("")
				#self.lblHeaderROMChecksumResult.setText("")
				self.cmbHeaderROMSizeResult.setCurrentIndex(11)
				self.cmbHeaderRAMSizeResult.setCurrentIndex(0)
				self.cmbHeaderFeaturesResult.setCurrentIndex(0)
			else:
				self.lblHeaderTitleResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
			
			self.grpAGBCartridgeInfo.setVisible(False)
			self.grpDMGCartridgeInfo.setVisible(True)
		
		elif self.CONN.GetMode() == "AGB":
			self.cmbAGBCartridgeTypeResult.clear()
			self.cmbAGBCartridgeTypeResult.addItems(self.CONN.GetSupportedCartridgesAGB()[0])
			self.cmbAGBCartridgeTypeResult.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
			if "flash_type" in data:
				self.cmbAGBCartridgeTypeResult.setCurrentIndex(data["flash_type"])

			self.lblAGBHeaderTitleResult.setText(data['game_title'])
			self.lblAGBHeaderCodeResult.setText(data['game_code'])
			self.lblAGBHeaderVersionResult.setText(str(data['version']))
			if data['logo_correct']:
				self.lblAGBHeaderLogoValidResult.setText("OK")
				self.lblAGBHeaderLogoValidResult.setStyleSheet(self.lblAGBHeaderCodeResult.styleSheet())
			else:
				self.lblAGBHeaderLogoValidResult.setText("Invalid")
				self.lblAGBHeaderLogoValidResult.setStyleSheet("QLabel { color: red; }");

			if data['96h_correct']:
				self.lblAGBHeader96hResult.setText("OK")
				self.lblAGBHeader96hResult.setStyleSheet(self.lblAGBHeaderCodeResult.styleSheet())
			else:
				self.lblAGBHeader96hResult.setText("Invalid")
				self.lblAGBHeader96hResult.setStyleSheet("QLabel { color: red; }");
			
			if data['header_checksum_correct']:
				self.lblAGBHeaderChecksumResult.setText("Valid (0x{:02X})".format(data['header_checksum']))
				self.lblAGBHeaderChecksumResult.setStyleSheet(self.lblAGBHeaderCodeResult.styleSheet())
			else:
				self.lblAGBHeaderChecksumResult.setText("Invalid (0x{:02X})".format(data['header_checksum']))
				self.lblAGBHeaderChecksumResult.setStyleSheet("QLabel { color: red; }");
			self.lblAGBHeaderROMChecksumResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
			self.lblAGBHeaderROMChecksumResult.setText("Not available")
			self.AGB_Global_CRC32 = 0
			
			db_agb_entry = None
			
			if os.path.exists("{0:s}/db_AGB.json".format(self.CONFIG_PATH)):
				with open("{0:s}/db_AGB.json".format(self.CONFIG_PATH)) as f:
					db_agb = f.read()
					db_agb = json.loads(db_agb)
					if data["header_sha1"] in db_agb.keys():
						db_agb_entry = db_agb[data["header_sha1"]]
					else:
						self.lblAGBHeaderROMChecksumResult.setText("Not in database")
			else:
				print("FAIL: Database for Game Boy Advance titles not found in " + "{0:s}/db_AGB.json".format(self.CONFIG_PATH))
			
			if db_agb_entry != None:
				self.cmbAGBHeaderROMSizeResult.setCurrentIndex(self.AGB_Header_ROM_Sizes_Map.index(db_agb_entry['rs']))
				if data["rom_size_calc"] < 0x400000:
					self.lblAGBHeaderROMChecksumResult.setText("In database (0x{:06X})".format(db_agb_entry['rc']))
					self.AGB_Global_CRC32 = db_agb_entry['rc']
			
			elif data["rom_size"] != 0:
				if not data["rom_size"] in self.AGB_Header_ROM_Sizes_Map:
					data["rom_size"] = 0x2000000
				self.cmbAGBHeaderROMSizeResult.setCurrentIndex(self.AGB_Header_ROM_Sizes_Map.index(data["rom_size"]))
			else:
				self.cmbAGBHeaderROMSizeResult.setCurrentIndex(0)
			
			if data["save_type"] == None:
				self.cmbAGBSaveTypeResult.setCurrentIndex(0)
				if db_agb_entry != None:
					if db_agb_entry['st'] < len(self.AGB_Header_Save_Types):
						self.cmbAGBSaveTypeResult.setCurrentIndex(db_agb_entry['st'])
			
			if data['empty'] == True: # defaults
				self.lblAGBHeaderTitleResult.setText("(No ROM data detected)")
				self.lblAGBHeaderTitleResult.setStyleSheet("QLabel { color: red; }");
				#self.lblAGBHeaderCodeResult.setText("")
				#self.lblAGBHeaderVersionResult.setText("")
				#self.lblAGBHeaderLogoValidResult.setText("")
				#self.lblAGBHeader96hResult.setText("")
				#self.lblAGBHeaderChecksumResult.setText("")
				#self.lblAGBHeaderROMChecksumResult.setText("")
				self.cmbAGBHeaderROMSizeResult.setCurrentIndex(3)
				self.cmbAGBSaveTypeResult.setCurrentIndex(0)
			else:
				self.lblAGBHeaderTitleResult.setStyleSheet(self.lblHeaderCGBResult.styleSheet())
			
			self.grpDMGCartridgeInfo.setVisible(False)
			self.grpAGBCartridgeInfo.setVisible(True)
		
		if resetStatus:
			self.lblStatus1aResult.setText("–")
			self.lblStatus2aResult.setText("–")
			self.lblStatus3aResult.setText("–")
			self.lblStatus4a.setText("Ready.")
			self.grpStatus.setTitle("Transfer Status")
			self.FinishOperation()
		
		if self.CONN.CheckROMStable() is False:
			QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "Unstable ROM reading detected. Please make sure that the cartridge contacts are very clean and that you selected the correct mode.", QtWidgets.QMessageBox.Ok)
			return
		
		if not data['logo_correct'] and data['empty'] == False:
			QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "The Nintendo Logo check failed which usually means that the cartridge couldn’t be read correctly. Please make sure that the cartridge contacts are very clean and that you selected the correct mode.", QtWidgets.QMessageBox.Ok)
		
		if data['game_title'][:11] == "YJencrypted":
			QtWidgets.QMessageBox.warning(self, "{:s} {:s}".format(APPNAME, VERSION), "This cartridge may be protected against reading or writing a ROM. If you don’t want to risk this cartridge to render itself unusable, please do not try to write a new ROM to it.", QtWidgets.QMessageBox.Ok)

	def formatFileSize(self, size):
		size = size / 1024
		if size < 1024:
			return "{:.1f} KB".format(size)
		else:
			return "{:.2f} MB".format(size/1024)

	def formatProgressTime(self, sec):
		if int(sec) == 1:
			return "{:d} second".format(int(sec))
		elif sec < 60:
			return "{:d} seconds".format(int(sec))
		elif int(sec) == 60:
			return "1 minute"
		else:
			min = int(sec / 60)
			sec = int(sec % 60)
			s = str(min) + " "
			if min == 1:
				s = s + "minute"
			else:
				s = s + "minutes"
			s = s + ", " + str(sec) + " "
			if sec == 1:
				s = s + "second"
			else:
				s = s + "seconds"
			return s
	
	def SetProgress(self, args):
		self.MUTEX.acquire(1)
		try:
			if not "method" in self.PROGRESS: self.PROGRESS = {}
			now = time.time()
			if args["action"] == "INITIALIZE":
				self.PROGRESS["method"] = args["method"]
				self.PROGRESS["size"] = args["size"]
				if "pos" in args:
					self.PROGRESS["pos"] = args["pos"]
				else:
					self.PROGRESS["pos"] = 0
				if "time_start" in args:
					self.PROGRESS["time_start"] = args["time_start"]
				else:
					self.PROGRESS["time_start"] = now
				self.PROGRESS["time_last_emit"] = now
				self.PROGRESS["time_last_update_speed"] = now
				self.PROGRESS["time_left"] = 0
				self.PROGRESS["speed"] = 0
				self.PROGRESS["speeds"] = []
				self.PROGRESS["bytes_last_update_speed"] = 0
				if args["method"] == "ROM_READ":
					self.grpStatus.setTitle("Transfer Status (Backup ROM)")
				elif args["method"] == "ROM_WRITE":
					self.grpStatus.setTitle("Transfer Status (Flash ROM)")
				elif args["method"] == "ROM_WRITE_VERIFY":
					self.grpStatus.setTitle("Transfer Status (Verify Flash)")
				elif args["method"] == "SAVE_READ":
					self.grpStatus.setTitle("Transfer Status (Backup Save Data)")
				elif args["method"] == "SAVE_WRITE":
					self.grpStatus.setTitle("Transfer Status (Write Save Data)")
				self.UpdateProgress(self.PROGRESS)
			
			if args["action"] == "ABORT":
				self.UpdateProgress(args)
				self.grpStatus.setTitle("Transfer Status")
				self.PROGRESS = {}
			
			elif args["action"] in ("ERASE", "SECTOR_ERASE"):
				if "time_start" in self.PROGRESS:
					args["time_elapsed"] = now - self.PROGRESS["time_start"]
				elif "time_start" in args:
					args["time_elapsed"] = now - args["time_start"]
				args["pos"] = 1
				args["size"] = 0
				self.UpdateProgress(args)
			
			elif self.PROGRESS == {}:
				return
			
			elif args["action"] == "UPDATE_POS":
				self.PROGRESS["pos"] = args["pos"]
				self.UpdateProgress(self.PROGRESS)
			
			elif args["action"] in ("READ", "WRITE"):
				if "method" not in self.PROGRESS: return
				elif args["action"] in ("READ") and self.PROGRESS["method"] in ("SAVE_WRITE", "ROM_WRITE"): return
				elif args["action"] in ("WRITE") and self.PROGRESS["method"] in ("SAVE_READ", "ROM_READ", "ROM_WRITE_VERIFY"): return
				if self.PROGRESS["pos"] >= self.PROGRESS["size"]: return
				
				self.PROGRESS["pos"] += args["bytes_added"]
				if (now - self.PROGRESS["time_last_emit"]) > 0.05:
					self.PROGRESS["time_elapsed"] = now - self.PROGRESS["time_start"]
					if (now - self.PROGRESS["time_last_update_speed"]) > 0.25:
						time_delta = now - self.PROGRESS["time_last_update_speed"]
						pos_delta = self.PROGRESS["pos"] - self.PROGRESS["bytes_last_update_speed"]
						if time_delta > 0:
							speed = (pos_delta / time_delta) / 1024
							self.PROGRESS["speeds"].append(speed)
							if len(self.PROGRESS["speeds"]) > 256: self.PROGRESS["speeds"].pop(0)
							self.PROGRESS["speed"] = statistics.median(self.PROGRESS["speeds"])
						self.PROGRESS["time_last_update_speed"] = now
						self.PROGRESS["bytes_last_update_speed"] = self.PROGRESS["pos"]
					
					if "skipping" in args and args["skipping"] is True:
						self.PROGRESS["speed"] = 0
						self.PROGRESS["skipping"] = True
					else:
						self.PROGRESS["skipping"] = False
					
					if self.PROGRESS["speed"] > 0:
						total_speed = statistics.mean(self.PROGRESS["speeds"])
						self.PROGRESS["time_left"] = (self.PROGRESS["size"] - self.PROGRESS["pos"]) / 1024 / total_speed
					
					self.UpdateProgress(self.PROGRESS)
					self.PROGRESS["time_last_emit"] = now
			
			elif args["action"] == "FINISHED":
				self.PROGRESS["pos"] = self.PROGRESS["size"]
				self.UpdateProgress(self.PROGRESS)
				qt_app.processEvents()
				self.PROGRESS["action"] = args["action"]
				self.PROGRESS["bytes_last_update_speed"] = self.PROGRESS["size"]
				self.PROGRESS["time_elapsed"] = now - self.PROGRESS["time_start"]
				self.PROGRESS["time_last_emit"] = now
				self.PROGRESS["time_last_update_speed"] = now
				self.PROGRESS["time_left"] = 0
				self.PROGRESS["speed"] = (self.PROGRESS["size"] / self.PROGRESS["time_elapsed"]) / 1024
				self.PROGRESS["bytes_last_emit"] = self.PROGRESS["size"]
				if "verified" in args: self.PROGRESS["verified"] = (args["verified"] == True)
				
				if self.PROGRESS["speed"] > self.PROGRESS["size"] / 1024:
					self.PROGRESS["speed"] = self.PROGRESS["size"] / 1024

				self.UpdateProgress(self.PROGRESS)
				del(self.PROGRESS["method"])
		
		finally:
			self.MUTEX.release()
	
	def UpdateProgress(self, args):
		if args is None: return
		
		if "error" in args:
			self.lblStatus4a.setText("Failed!")
			self.grpDMGCartridgeInfo.setEnabled(True)
			self.grpAGBCartridgeInfo.setEnabled(True)
			self.grpActions.setEnabled(True)
			self.btnCancel.setEnabled(False)
			msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Critical, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text=str(args["error"]), standardButtons=QtWidgets.QMessageBox.Ok)
			if not '\n' in str(args["error"]): msgbox.setTextFormat(QtCore.Qt.RichText)
			msgbox.exec()
			return
		
		self.grpDMGCartridgeInfo.setEnabled(False)
		self.grpAGBCartridgeInfo.setEnabled(False)
		self.grpActions.setEnabled(False)
		
		pos = 0
		size = 0
		speed = 0
		elapsed = 0
		left = 0
		if "pos" in args: pos = args["pos"]
		if "size" in args: size = args["size"]
		if "speed" in args: speed = args["speed"]
		if "time_elapsed" in args: elapsed = args["time_elapsed"]
		if "time_left" in args: left = args["time_left"]
		
		if "action" in args:
			if args["action"] == "ERASE":
				self.lblStatus1aResult.setText("Pending...")
				self.lblStatus2aResult.setText("Pending...")
				self.lblStatus3aResult.setText(self.formatProgressTime(elapsed))
				self.lblStatus4a.setText("Erasing flash...")
				self.lblStatus4aResult.setText("")
				self.btnCancel.setEnabled(args["abortable"])
				self.SetProgressBars(min=0, max=size, value=pos)
			elif args["action"] == "SECTOR_ERASE":
				if elapsed >= 1:
					self.lblStatus3aResult.setText(self.formatProgressTime(elapsed))
				self.lblStatus4a.setText("Erasing sector...")
				self.lblStatus4aResult.setText("")
				self.btnCancel.setEnabled(args["abortable"])
				self.SetProgressBars(min=0, max=size, value=pos)
			elif args["action"] == "ABORTING":
				self.lblStatus1aResult.setText("–")
				self.lblStatus2aResult.setText("–")
				self.lblStatus3aResult.setText("–")
				self.lblStatus4a.setText("Stopping... Please wait.")
				self.lblStatus4aResult.setText("")
				self.btnCancel.setEnabled(args["abortable"])
				self.SetProgressBars(min=0, max=size, value=pos)
			elif args["action"] == "FINISHED":
				self.FinishOperation()
			elif args["action"] == "ABORT":
				wd = 10
				while self.CONN.WORKER.isRunning():
					time.sleep(0.1)
					wd -= 1
					if wd == 0: break
					pass
				self.CONN.CANCEL = False
				self.grpDMGCartridgeInfo.setEnabled(True)
				self.grpAGBCartridgeInfo.setEnabled(True)
				self.grpActions.setEnabled(True)
				self.lblStatus1aResult.setText("–")
				self.lblStatus2aResult.setText("–")
				self.lblStatus3aResult.setText("–")
				self.lblStatus4a.setText("Stopped.")
				self.lblStatus4aResult.setText("")
				self.btnCancel.setEnabled(False)
				self.SetProgressBars(min=0, max=1, value=0)
				self.btnCancel.setEnabled(False)
				
				if "info_type" in args.keys() and "info_msg" in args.keys():
					if args["info_type"] == "msgbox_critical":
						msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Critical, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text=args["info_msg"], standardButtons=QtWidgets.QMessageBox.Ok)
						if not '\n' in args["info_msg"]: msgbox.setTextFormat(QtCore.Qt.RichText)
						msgbox.exec()
					elif args["info_type"] == "msgbox_information":
						msgbox = QtWidgets.QMessageBox(parent=self, icon=QtWidgets.QMessageBox.Information, windowTitle="{:s} {:s}".format(APPNAME, VERSION), text=args["info_msg"], standardButtons=QtWidgets.QMessageBox.Ok)
						if not '\n' in args["info_msg"]: msgbox.setTextFormat(QtCore.Qt.RichText)
						msgbox.exec()
					elif args["info_type"] == "label":
						self.lblStatus4a.setText(args["info_msg"])
				
				return
		
		else:
			self.SetProgressBars(min=0, max=size, value=pos)
			self.btnCancel.setEnabled(True)
			self.lblStatus1aResult.setText(self.formatFileSize(pos))
			if speed > 0:
				self.lblStatus2aResult.setText("{:.2f} KB/s".format(speed))
			else:
				self.lblStatus2aResult.setText("Pending...")
			if left > 0:
				self.lblStatus4aResult.setText(self.formatProgressTime(left))
			else:
				self.lblStatus4aResult.setText("Pending...")
			if elapsed > 0:
				self.lblStatus3aResult.setText(self.formatProgressTime(elapsed))

			if speed == 0 and "skipping" in args and args["skipping"] is True:
				self.lblStatus4aResult.setText("Pending...")
			self.lblStatus4a.setText("Time left:")
	
	def SetProgressBars(self, min=0, max=100, value=0, setPause=None):
		self.prgStatus.setMinimum(min)
		self.prgStatus.setMaximum(max)
		self.prgStatus.setValue(value)
		if self.TBPROG is not None:
			if not value > max:
				self.TBPROG.setRange(min, max)
				self.TBPROG.setValue(value)
				if value != min and value != max:
					self.TBPROG.setVisible(True)
				else:
					self.TBPROG.setVisible(False)
			if setPause is not None:
				self.TBPROG.setPaused(setPause)
			else:
				self.TBPROG.setPaused(False)
	
	def ShowPocketCameraWindow(self):
		self.CAMWIN = None
		self.CAMWIN = PocketCameraWindow(self, icon=self.windowIcon())
		self.CAMWIN.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
		self.CAMWIN.setModal(True)
		self.CAMWIN.run()
	
	def dragEnterEvent(self, e):
		if self._dragEventHover(e):
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
		if self._dragEventHover(e):
			e.accept()
		else:
			e.ignore()

	def _dragEventHover(self, e):
		if self.btnHeaderRefresh.isEnabled() and self.grpActions.isEnabled() and e.mimeData().hasUrls:
			for url in e.mimeData().urls():
				if platform.system() == 'Darwin':
					fn = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
				else:
					fn = str(url.toLocalFile())
				
				fn_split = os.path.splitext(os.path.abspath(fn))
				if fn_split[1] == ".sav":
					return True
				elif self.CONN.GetMode() == "DMG" and fn_split[1] in (".gb", ".sgb", ".gbc", ".bin"):
					return True
				elif self.CONN.GetMode() == "AGB" and fn_split[1] in (".gba", ".srl"):
					return True
				else:
					return False
		return False
	
	def dropEvent(self, e):
		if self.btnHeaderRefresh.isEnabled() and self.grpActions.isEnabled() and e.mimeData().hasUrls:
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
			for url in e.mimeData().urls():
				if platform.system() == 'Darwin':
					fn = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
				else:
					fn = str(url.toLocalFile())
				
				fn_split = os.path.splitext(os.path.abspath(fn))
				if fn_split[1] in (".gb", ".sgb", ".gbc", ".bin", ".gba", ".srl"):
					self.FlashROM(fn)
				elif fn_split[1] == ".sav":
					self.WriteRAM(fn)
		else:
			e.ignore()

	def closeEvent(self, event):
		self.DisconnectDevice()
		event.accept()
	
	def run(self):
		self.layout.update()
		self.layout.activate()
		screen = QtGui.QGuiApplication.screens()[0]
		screenGeometry = screen.geometry()
		x = (screenGeometry.width() - self.width()) / 2
		y = (screenGeometry.height() - self.height()) / 2
		self.move(x, y)
		self.setAcceptDrops(True)
		self.show()
		
		# Taskbar Progress on Windows only
		try:
			from PySide2.QtWinExtras import QWinTaskbarButton, QtWin
			myappid = 'lesserkuma.flashgbx'
			QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
			taskbar_button = QWinTaskbarButton()
			self.TBPROG = taskbar_button.progress()
			self.TBPROG.setRange(0, 100)
			taskbar_button.setWindow(self.windowHandle())
			self.TBPROG.setVisible(False)
		except ImportError:
			pass
		
		qt_app.exec_()

def main(portableMode=False):
	if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
		app_path = os.path.dirname(sys.executable)
	else:
		app_path = os.path.dirname(os.path.abspath(__file__))
	
	cp = { "subdir":app_path + "/config", "appdata":QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppConfigLocation) }
	
	if portableMode:
		cfgdir_default = "subdir"
	else:
		cfgdir_default = "appdata"
	
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--reset", help="clears all settings such as last used directory information", action="store_true")
	parser.add_argument("--cfgdir", choices=["appdata", "subdir"], type = str.lower, default=cfgdir_default, help="sets the config directory to either the OS-provided local app config directory (" + cp['appdata'] + "), or a subdirectory of this application (" + cp['subdir'].replace("\\", "/") + ")")
	args = parser.parse_args()
	config_path = cp[args.cfgdir]
	
	print("{:s} {:s} by Lesserkuma".format(APPNAME, VERSION))
	print("\nDISCLAIMER: This software is provided as-is and the developer is not responsible for any damage that is caused by the use of it. Use at your own risk!")
	print("\nFor troubleshooting please visit https://github.com/lesserkuma/FlashGBX")
	
	app = FlashGBX({"app_path":app_path, "config_path":config_path, "argparsed":args})
	app.run()

qt_app = QtWidgets.QApplication(sys.argv)
qt_app.setApplicationName(APPNAME)
