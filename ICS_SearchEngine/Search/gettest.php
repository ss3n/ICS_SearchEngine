<?php
$searchquery=$_POST['searchbox'];
$words=explode(" ", $searchquery);

//Build a parameterized query to pass through GET. Adding a + between each pair of words
$result="";
foreach ($words as $word) 
{
	if($result=="") {$result=$result.$word;}
	else
	{
		$result=$result."+".$word;
	}
}

//The URL is the address at which our backend server is located
$URL="0.0.0.0:2564/query=";
$parameterized_query=$URL.$result;

echo $parameterized_query;

$ch = curl_init();
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_URL,$parameterized_query);
$content = curl_exec($ch);
echo $content;

?>