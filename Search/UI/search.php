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
			$i=0;
			if($obj=json_decode($content, true) and $i<20)
			{
				foreach($obj['items'] as $iteminstance)
					{	
						$i+=1;
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
				echo "<p>Json is not valid</p>";
			}

			///////////////Google results code - retrieves top 5 google results and sends it to python server////

			$result=$result."+site:ics.uci.edu";

			//echo $result;
			
			//The googleURL is the address at which Google Ajax API is located
			//$googleURL="https://www.googleapis.com/customsearch/v1?key=AIzaSyARRvhnIx6GhTYAssClqi-Befnx958T4ms&q=";
			$googleURL="https://www.googleapis.com/customsearch/v1?key=AIzaSyC0NNGclMTrbs0zcdnfXVDE2VJiGuVj5TY&cx=004495725010310928265:i8_5au6lyco&q=";


			//$googleURL="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=";
			$google_parameterized_query=$googleURL.$result;

			//echo $parameterized_query;

			$ch = curl_init();
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
			curl_setopt($ch, CURLOPT_URL,$google_parameterized_query);
			$content = curl_exec($ch);
			//echo $content;


			$json=json_decode($content,true);
			$google_results_for_python="";

			$i=0;
			foreach ($json['items'] as $iteminstance)
			{
				if($i>=5) break;
				//just fetch items[link] and print it
			if ($google_results_for_python=="")
				{
					$non_html_flag=preg_match('#css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4|txt|gz|py
												|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf
												|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1
												|thmx|mso|arff|rtf|jar|csv
												|rm|smil|wmv|swf|wma|zip|rar|gz#',$iteminstance['link']);
					if(!$non_html_flag)
					{
						$google_results_for_python=$google_results_for_python.$iteminstance['link'];
						$i+=1;
					}
				}
			else
				{
					$non_html_flag=preg_match('#css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4|txt|gz|py
												|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf
												|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1
												|thmx|mso|arff|rtf|jar|csv
												|rm|smil|wmv|swf|wma|zip|rar|gz#',$iteminstance['link']);
					if(!$non_html_flag)
					{
						$google_results_for_python=$google_results_for_python."###".$iteminstance['link'];
						$i+=1;
					}
				}

			}

				
			//echo "Google results are as follows separated by a ###: ".$google_results_for_python;
			$google_results_for_python="0.0.0.0:2564/googleresults=".$google_results_for_python;

			//echo $google_results_for_python;

			curl_setopt($ch, CURLOPT_URL,$google_results_for_python);
			//$content = curl_exec($ch);



			//if ($content)
			//{
				//print_r("Successfully sent google results to python");
			//}

			///////Google results code ends here/////////////

			?>

			<div id="footer"><a href="#">Jump to top</a></div>
			</div>
		</div>
	</body>
</html>