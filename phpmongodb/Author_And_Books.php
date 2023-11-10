<?php
    include_once('connect.php');

    $query = [['$unwind'=> '$author_information'], ['$group'=> ['_id'=> ['author'=> '$author_information._Name'], 'num_books'=> ['$sum'=> 1]]], ['$project'=> [ '_id'=> 0, 'author'=> '$_id.author', 'num_books'=> 1]], ['$sort' => ['num_books'=> -1]]];

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
            <th colspan="2"><h2>Amount of Books for each Author</h2></th>
        </tr>
        <t>
            <th> Author </th>
            <th> Number of Books </th>
        </t>

    <?php 
        for ($x = 0; $x < 15; $x++){
    ?>
        <tr>
            <td style="text-align:center"><?php echo $array[$x]['author']; ?></td>
            <td style="text-align:center"><?php echo $array[$x]['num_books']; ?></td>
        </tr>
    <?php    
        }
     ?>
     </table>
</body>
</html>