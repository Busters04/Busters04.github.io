<?php
    include_once('connect.php');

    $query = [['$unwind'=> '$author_information'], ['$group'=> ['_id'=> '$author_information._Name', 'total_value'=> ['$sum'=> '$_Book_Cost']]], ['$project'=> [ '_id'=> 0, 'author'=> '$_id', 'total_value'=> 1]], ['$sort'=> ['total_value'=> -1]]];

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
    <table align="center" border="1px" style="width:600px; line-height:40px;">
        <tr>
            <th colspan="2"><h2>Value of all Authors Books</h2></th>
        </tr>
        <t>
            <th> Author </th>
            <th> All Books Cost </th>
        </t>

    <?php 
        for ($x = 0; $x < 15; $x++){
    ?>
        <tr>
            <td style="text-align:center"><?php echo $array[$x]['author']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['total_value']; ?></td>
        </tr>
    <?php    
        }
     ?>
     </table>
</body>
</html>
