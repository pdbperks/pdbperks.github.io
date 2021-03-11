<?php 
header("Cache-Control: no-cache");
session_start();

//$used= $_SESSION['used'];//$_GET['used'];
//if ($routine==NULL) $routine='splash';
//$site="http://".$_SERVER['SERVER_ADDR'];
$site="http://".$_SERVER['SERVER_NAME'];

$self = $_SERVER['PHP_SELF'];
?>

<HTML>
<HEAD>
<TITLE>Real Perks</TITLE>
<META NAME="description"CONTENT="objects to poetry.">
<META NAME="owner"CONTENT="david@dperks.co.uk">
<META NAME="author"CONTENT="pdbperks">
<META NAME="keywords"CONTENT="pic art maker">
<style>
@import url("../css/blog.css");
</style>

</HEAD>

<BODY BGCOLOR="#000000"text="#666666"LINK="#9999a6"ALINK="#808080"VLINK="#666666">


<a href = "../index.php"><IMG id="headIcon"
align=right WIDTH=32 HEIGHT=38 BORDER=0
ALT="Perks" SRC="../head.gif"></A>


<h2>Kinect to GIMP.</h2><p align=left>

<?php

echo <<<END

<p>
<div class='dateTitle'>Friday 29 June 2018. Introduction.</div>
<p>
The first time I used Python scripting in 2014, it was to create extensions for the opensource graphics program GIMP. <p>

I created a <a href='dropShadow.py'>drop shadow text widget</a>:
<p>
<img src='images/welcome1.PNG'>

<img src='images/welcome2.PNG'>
<p>
I think I need to work on the default settings!
<p>
<p>
<div class='dateTitle'>Friday 29 June 2018. Kinect.</div>
<p>
I bought an XBOX360 Kinect sensor from a carboot sale for �2.50 and was interested to see how I could access it using my new knowledge of Python scripting.  I had previously hacked the Kinect sensor using OpenKinect and Flex2 but saw greater potential if I could access it with Python.  Since I am mostly working on Win10 these days, I also wanted to use the official <a href = 'https://www.microsoft.com/en-gb/download/details.aspx?id=40278'>Microsoft Kinect API</a>. 
<p>
<img src='images/kinect.jpg'>
<p>
I believe that Microsoft have ceased production of Kinect sensors (both 360 and One versions) but pykinect can still be found hosted on <a href='https://github.com/Microsoft/PTVS/wiki/PyKinect'> GitHub</a> with the relevant <a href='https://github.com/Microsoft/PTVS/tree/master/Python/Product/PyKinect/PyKinect/pykinect'>module files at this address</a>. 
<p>
Pykinect is written for Python2 and I have been working with Python3 so I had a look at <a href='https://github.com/ShrirangaKadam/pykinect-python3.6'>pykinect for python3.6</a> but with only partial success.  It would be nice to get this workiing fully but I spent a week becoming frustrated by the fact that I could get the depth and video images working but not the skeleton data: or with a bit of creative adjustment, the skeleton data but not the images. 
<p>
It would have been sensible before reaching this point of frustration to test pyKinect from Python2 but I was hesitant to spoil my Python3 install.
<p>
<div class='dateTitle'>Friday 29 June 2018. Remember GIMP.</div>
<p>
During an idle moment sketching on <a href='http://mypaint.org/'>MyPaint</a> I started thinking that it would be nice to interface the kinect with a graphics program.  I then remembered my experiements with GIMP: I already had experience of using the python-fu script interface and that used Python2.7 as a discreet install. 
<p>
I was struggling to install pygame in the GIMP distribution. Although simple module files could be pasted into <code>C:\Program Files\GIMP 2\Python\Lib\site-packages\</code> folder, more complex modules would require a pip install.  I couldn't use pip from Python3 and the GIMP install didn't have pip modules.  So I installed a new version of <a href='https://www.python.org/download/releases/2.7/'>Python2.7</a> into the GIMP folder next to the application install of Python and copied the pip modules across. Using <code>python -m pip install</code> I was able to install pygame and test the <a href='https://github.com/Microsoft/PTVS/blob/master/Python/Product/PyKinect/PyKinect/PyGameDemo.py'>pygamedemo</a>.  I created an alias to run Python2 from PowerShell and the demo worked perfectly first time.  I shall probably merge these two installs in time.
<p>
Taking another look at my earlier experiments in GIMP and <a href='https://www.gimp.org/docs/python/index.html'>this useful guide</a>, I was able to run the pygamedemo from within GIMP and use the kinect data SkeletonPositions[JointId.HandRight] to draw into a  GIMP window.
<p>
<img src='images/gimp.png'>
<p>
Essentially the main code has been moved into a function which is called by the gimpfu register block. I have added a brush on/off control through an overlapping hand gesture but the interface is still simple in <a href ='gameK.py'>this example of the code</a>.  Adjustment of colour and brush is still handled by the GIMP gui. The results are satisfactory but the lack of precision is not very inspiring for future development.  
<p>
<img src='images/example01.png'><img src='images/example02.png'><img src='images/example03.png'><img src='images/example04.png'>

<p>
<div class='dateTitle'>Tueday 3 July 2018. Refinement.</div>
<p>
I set the window proportions to match the Kinect depth image.  I changed the brush mark to dot rather than line which works better with a larger brush and lower opacity. Exploring brush pattern and paint effect also work with this gestural interface. I am far more optimistic about this interface and want to explore startup options and depth to layer painting.
<p>
<img src='images/example09.png'><img src='images/example08.png'>
<p>
<div class='dateTitle' id='layers'>Saturday 7 July 2018. Layers.</div>
<p>
The <a href ='gameKlayers.py'>current code</a> creates four paint layers; the active layer being determined by distance from the sensor.  The left hand is now used to change the brush size rather than acting as an on/off switch. 
<p>
<img src='images/example10.png'><img src='images/example16.png'>
<p>
The brush size can be corellated directly with the Y axis. In this instance, divided by two as a positive float number. 
<pre>pdb.gimp_context_set_brush_size(abs(float(LHand[1]/2)))</pre>
<p>
Initial paint tests show this to be a natural combination of movements and the brush can be effectively turned off by raising the left hand to zero.
<p>
I am considering selecting the colour through depth position. This might be an alternative or subfunction of the layer feature, possibly selected  through a widget at startup. Another alternative would be to have a palette selection at the top of the pygame skeleton screen.

<p>
<div class='dateTitle' id='color'>Monday 9 July 2018. Palette.</div>
<p>
A list of rectangles is drawn on the pygame window prior to the skeleton routine.  <code>if item.collidepoint(LHand):</code> is used to check if the left hand is touching a rectangle and selects the colour. 
<p>
<img src='images/gimp2.png'>
<p>
<a href ='gameKcolour.py'>The code</a> would now benefit from some refinement and commenting 
but the colour palette works well and improves the painting experience.  The palette could be set at loading and other features such as brush shape or eraser could be selected on screen.


<A NAME="end"></A>
END
?>


<hr>
<p>

</center>
</body>