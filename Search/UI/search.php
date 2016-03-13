<!DOCTYPE html>
<?php
$searchquery=$_POST['searchbox'];
?>
<html>
	<head>
		<meta name="author" content="Arjun, Shiladitya, Swarun"/>
		<link rel="stylesheet" href="searchstyle.css"/>
		<title>Search Engine</title>
	</head>
	<body>
		<div class="wrap">
			<form action="search.php" method="post">
				<div id="textandbutton">
					<?php echo '<input id="thesearchbar" title="Search text goes here" type="textbox" name="searchbox" placeholder="Search string goes here" value="'.$searchquery.'" />';
					?>
					<button class="thebutton" type="submit"/>
				</div>
			</form>
			<div class="content">
			
			<?php
			
			
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

			//echo $parameterized_query;

			$ch = curl_init();
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
			curl_setopt($ch, CURLOPT_URL,$parameterized_query);
			$content = curl_exec($ch);
			//echo $content;

			if($obj=json_decode($content, true))
			{
				foreach($obj['items'] as $iteminstance)
					{
						$final_string_to_display= '<div class="item"><div class="itemheading"><h3><a href="'.$iteminstance["itemURL"].'">'.$iteminstance['itemheading'].'</a></h3></div><div class="itemcontent">'.$iteminstance['itemcontent'].'</div></div>';
						foreach ($words as $word) 
						{
							$final_string_to_display= preg_replace($matched='#'.$word.'#i', $replacement='<span class="bolded">'.$word.'</span>', $final_string_to_display);
							//echo " ".$matched." replaced=".$replacement;
						}
						echo $final_string_to_display;
					}
			}

			else
			{
				echo "Json is not valid :(";
			}
			?>

			<div id="footer"><a href="#">Jump to top</a></div>
			</div>
		</div>
	</body>
</html>