<?php
    include_once('connect.php');

    $query = [['$unwind'=> '$author_information'], [ '$sort' => ['_Book_Cost'=> 1]]];

    $result = $book_information->aggregate($query);

    $objects = json_decode(json_encode($result->toArray(),true));

    $array=json_decode(json_encode($objects),true);

    //$author_information = $book_information->author_information;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eli's Bookstore</title>
</head>
<body>
    <table align="center" border="1px" style="width:1200px; line-height:40px;">
        <tr>
            <th colspan="7"><h2>Books Ordered By Cost</h2></th>
        </tr>
        <t>
            <th> Book Title </th>
            <th> Book Genre </th>
            <th> Publisher's Name </th>
            <th> Year Published </th>
            <th> ISBN Number </th>
            <th> Cost of Book </th>
            <th> Authors </th>
        </t>

    <?php 
        for ($x = 0; $x < 26; $x++){
    ?>
        <tr>
            <td style="text-align:center"><?php echo $array[$x]['_Title']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['_Genre']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['_Publisher_Name']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['_Year_Published']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['_ISBN']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['_Book_Cost']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['author_information']['_Name']; echo "<br>"; for ($y = 1; $y < 3; $y++){ if ($x < 24 and $array[$x]['_ID'] == $array[$x + $y]['_ID']){ echo $array[$x+$y]['author_information']['_Name']; $x += $y;}}?></td>
        </tr>
    <?php    
        }
     ?>
     </table>
</body>
</html>