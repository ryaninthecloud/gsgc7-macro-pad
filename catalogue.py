'''
Catalogue of response options

Patterns for defining functions to be called
--------------------------------------------
After some thinking, it might be better to do
lambda definitions for things like prints so that
parsing a command can be done somewhat more easily.

x = {'y': lambda a,b: print (a+b)} <-- pattern for prints
Called in interface by x['y']('1','2') --> returns '12'
'''
from os import system

def windows_focus_app(application_name: str):
    '''
    Used to put an application in focus if it
    is already open

    Args:
        application_name (str): application to focus
    Returns:
        None
    '''
    system(f"""powershell.exe -command\
            $wshell = New-Object -ComObject wscript.shell;\
            $wshell.AppActivate('{application_name}');\
            """)

def windows_send_keystroke(stroke_to_send: str):
    '''
    Used to send a particular keystroke
    to Windows via Powershell. Is it slow? Yes.
    Does it work? Yes. And that's what this project
    is all about. Otherwise I'd just buy a Macro keypad.
    
    Args:
        stroke_to_send (str): keystroke to send
    Returns:
        None
    '''
    system(f"""powershell.exe $wshell = New-Object -ComObject wscript.shell;\
            $wshell.SendKeys('{stroke_to_send}')""")

def windows_focus_and_control(app_to_focus: str, stroke_to_send: str):
    '''
    A combined function using the same WShell instance
    to call an app to focus an then send a keystroke

    Args:
        app_to_focus (str): name of app to focus
        stroke_to_send (str): keystroke to send
    '''
    system(f"""powershell.exe -command\
            {app_to_focus}.exe;\
            $wshell = New-Object -ComObject wscript.shell;\
            $wshell.AppActivate('{app_to_focus}'); Sleep 0.5;\
            $wshell.SendKeys('{stroke_to_send}');\
            """)

windows_dispatch_catalogue = {
    'D' : {
        '1' : lambda: system('start wt.exe'),
        '2' : lambda: windows_focus_and_control('Spotify', ' '),
        '31' : lambda: [system(f'{app}') for app in ['start winword.exe','start outlook.exe','spotify','code']],
        '41' : lambda: system('explorer.exe https://portal.azure.com'),
        '#' : lambda: system('rundll32.exe user32.dll,LockWorkStation')
    },
    'H' : lambda : windows_send_keystroke('%{F4}')
}

macos_dispatch_catalogue = {

}