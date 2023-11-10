<?php
require 'vendor/autoload.php';

$client = new MongoDB\Client('mongodb://localhost:27017');
$mybookstore = $client->mybookstore;
$book_information = $mybookstore->book_information;

/*
foreach($mybookstore->listCollections()  as $collection)
{
    var_dump($collection);
}

$result1 = $mybookstore->createCollection("Book_information");

var_dump($result1);
*/
?>