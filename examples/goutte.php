// Replicated from the Goutte Documentation
// https://goutte.readthedocs.io/en/latest/
// Examples to make requests, click on liniks, extract data, and submit forms
require 'vendor/autoload.php';
use Goutte\Client;
$client = new Client();

// Make Requests using requests()
// Go to the symfony.com website
$crawler = $client->request('GET', 'http://www.symfony.com/blog/');

// Click on the "Security Advisories" link
$link = $crawler->selectLink('Security Advisories')->link();
$crawler = $client->click($link);

// Get the latest post in this category and display the titles
$crawler->filter('h2 > a')->each(function ($node) {
    print $node->text()."\n";
});

$crawler = $client->request('GET', 'http://github.com/');
$crawler = $client->click($crawler->selectLink('Sign in')->link());
$form = $crawler->selectButton('Sign in')->form();
$crawler = $client->submit($form, array('login' => 'fabpot', 'password' => 'xxxxxx'));
$crawler->filter('.flash-error')->each(function ($node) {
    print $node->text()."\n";
});

