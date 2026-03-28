<?php

$user = $_GET['username'] ?? '';
$pass = $_GET['password'] ?? '';

if ($user !== "josielluz" || $pass !== "3264717") {
    die("Acesso negado");
}

header("Content-Type: application/vnd.apple.mpegurl");

readfile("../docs/playlists.m3u");