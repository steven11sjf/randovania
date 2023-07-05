#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

F8::
stop := 0
idx := 0
Sleep 1000
Loop
{
	Send, {RAlt}
	Sleep 100
	Send, t
	Sleep 100
	Send, e
	Sleep 100
	Send, r
	Sleep 100
	Send, r
	Sleep 100
	Send, {Enter}
	Sleep 100
	Send, Brinstar
	Send, %idx%
	idx := idx + 1
	Sleep 100
	Send, {Enter}
	Sleep 100
	Send, {Tab}
	Sleep 50
	Send, {Enter}
	Sleep, 100
	Send, {right}
	Sleep, 100
}until stop
return

F9:: stop := 1