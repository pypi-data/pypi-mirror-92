ģ������: event - ����ʹ��import userevent !

��������: ������ʾ��:��������(examples\mouseController.py)
������ģ�� Included modules: 
============================

key.py - ģ������¼�
"""""""""""""""""""""
�����ĺ��� Functions:

keydown(keycode_or_keyname)::

    ģ������¡�
    keycode_or_keyname:�������ƻ�ð����ļ���ֵ

keypress(keycode_or_keyname, delay=0.05)::

    ģ�ⰴ����
    keycode_or_keyname:�������ƻ�ð����ļ���ֵ
    delay:���������ͷ�֮��ĵļ��ʱ��,���ʱ��ԽС,�����ٶ�Խ�졣

keyup(keycode_or_keyname)::

    ģ����ͷš�
    keycode_or_keyname:�������ƻ�ð����ļ���ֵ


mouse.py - ģ������¼�
"""""""""""""""""""""""
�����ĺ��� Functions:

click()::

    ģ������������

dblclick(delay=0.25)::

    ģ��������˫��

get_screensize()::

    ��ȡ��ǰ��Ļ�ֱ��ʡ�

getpos()::

    ��ȡ��ǰ���λ�á�
    ����ֵΪһ��Ԫ��,��(x,y)��ʽ��ʾ��

move(x, y)::

    ģ���ƶ���ꡣ
    ��goto��ͬ,move()*����*һ������¼���

right_click()::

    ģ������Ҽ�������

ʾ������1:
.. code-block:: python

    #ģ�ⰴ��Alt+F4�رյ�ǰ����
    from event.key import *
    keydown("Alt")
    keydown("f4")
    keyup("f4")
    keyup("alt")

ʾ������2:
.. code-block:: python

    #ʹ��Aero PeekԤ�����档(Win7������ϵͳ)
    from event import mouse
    x,y=mouse.get_screensize()
    mouse.move(x,y) #�����������Ļ���½�
    mouse.click() #ģ�������

���� Author:
*�߷ֳ��� qq:3076711200 ����:3416445406@qq.com*