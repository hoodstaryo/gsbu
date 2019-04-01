#include <GUIConstantsEx.au3>

AutoItSetOption("GUIOnEventMode", 1)

Func HandleGUIEventClose()
  Exit
EndFunc

Func Main()
  Local $green = "0x00ff00"
  Local $red = "0xff0000"
  Local $white = "0xffffff"
  Local $iterations = 100

  ; Show the window.
  GUICreate("Masher")
  GUISetOnEvent($GUI_EVENT_CLOSE, "HandleGUIEventClose")
  GUISetState(@SW_SHOW)

  ; Make the window red for 10 seconds.
  GUISetBkColor($red)
  Sleep(10000)
  GUISetBkColor($white)

  ; Flash.
  Sleep(1000)

  For $i = 1 To $iterations
    GUISetBkColor($green)
    Send("a")
    Sleep(100)
    GUISetBkColor($white)

    If $i <> $iterations Then Sleep(100)
  Next

  Sleep(1000) 

  ; Make the window red for 10 seconds.
  GUISetBkColor($red)
  Sleep(10000)
EndFunc

Main()
