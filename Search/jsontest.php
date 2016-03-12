<!DOCTYPE html>
<html>
<head>
<title> Testing json </title>
</head>

<body>

<div style="width:90%; float:left; overflow:auto; background-color:pink;">
<?php


$json=file_get_contents('searchdata.json');
//$json = str_replace('&quot;', '"', $json);
//$obj=json_decode(file_get_contents('searchdata.json'));

//echo $json;

if($obj=json_decode($json, true))
{
	//echo "hey its not empty!";
}

//else echo "it is empty :(";


foreach($obj['items'] as $iteminstance)
{
	echo "stuff:".$iteminstance['itemheading']." URL:".$iteminstance['itemURL']." Content:".$iteminstance['itemcontent'];
}

?>
</div>
</body>
</html>