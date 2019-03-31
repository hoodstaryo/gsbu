#include <GUIConstantsEx.au3>

AutoItSetOption("GUIOnEventMode", 1)

Main()

Func HandleGUIEventClose()
   Exit
EndFunc

Func Main()
   Local $green = "0x00ff00"
   Local $red = "0xff0000"
   Local $white = "0xffffff"

   GUICreate("Masher")
   GUISetOnEvent($GUI_EVENT_CLOSE, "HandleGUIEventClose")
   GUISetState(@SW_SHOW)

   GUISetBkColor($red)
   Sleep(10000)
   GUISetBkColor($white)
   Sleep(1000)

   For $i = 1 To 100
	  GUISetBkColor($green)
	  Send("a")
	  Sleep(100)
	  GUISetBkColor($white)
	  Sleep(1000)
   Next

   GUISetBkColor($red)
   Sleep(10000)
EndFunc