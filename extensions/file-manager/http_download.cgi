#!/usr/local/bin/perl

#
# Authentic Theme (https://github.com/authentic-theme/authentic-theme)
# Copyright Ilia Rostovtsev <ilia@virtualmin.com>
# Copyright Alexandr Bezenkov (https://github.com/real-gecko/filemin)
# Licensed under MIT (https://github.com/authentic-theme/authentic-theme/blob/master/LICENSE)
#

use strict;

our (%access, %in, %text, $cwd, $path);

require($ENV{'THEME_ROOT'}."/extensions/file-manager/file-manager-lib.pl");

if (!$in{'link'}) {
	redirect_local('list.cgi?path='.urlize($path).'&module=filemin'.extra_query());
	return;
	}

my ($host, $port, $page, $ssl) = parse_http_url($in{'link'});
if (!$host) {
	print_error($text{'error_invalid_uri'});
	}
else {
	my $file = $page;
	my $full;
	$file =~ s/^.*\///;
	$file ||= "index.html";
	$full = fm_checked_cwd_path_or_error($file);
	if (-e $full) {
		print_error(
			text('filemanager_rename_exists', $file, $path,
				$text{'theme_xhred_global_file'}).
			    "."
		);
		}
	else {
		my $success;
		my @st = stat($cwd);
		my ($address_mode, $allowed_addresses);
		if (defined(&check_download_address)) {
			$address_mode = $access{'download_address_mode'};
			$allowed_addresses = $access{'download_allowed_addresses'};
			}
		if ($ssl == 0 || $ssl == 1) {
			http_download($host, $port, $page, $full, undef, undef, $ssl,
				$in{'username'}, $in{'password'}, undef, undef, undef,
				undef, undef, $address_mode, $allowed_addresses);
			}
		else {
			ftp_download($host, $page, $full, undef, undef,
				$in{'username'}, $in{'password'}, $port, undef, undef,
				$address_mode, $allowed_addresses);
			}
		set_ownership_permissions($st[4], $st[5], undef, $full);
		@st = stat($cwd);
		$success .= text('http_done', nice_size($st[7]),
			"<tt>".html_escape($full)."</tt>");
		redirect_local('list.cgi?path='.
			    urlize($path).
			    '&module=filemin'.
			    '&success='.
			    $success.
			    extra_query());
		}
	}
