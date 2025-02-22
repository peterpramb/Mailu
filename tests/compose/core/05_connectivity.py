#!/usr/bin/env python3

import imaplib
import poplib
import smtplib
import os

SERVER='localhost'
USERNAME='user_UTF8@mailu.io'
PASSWORD='password€'
#https://github.com/python/cpython/issues/73936
#SMTPlib does not support UTF8 passwords.
USERNAME_ASCII='user@mailu.io'
PASSWORD_ASCII='password'


def test_imap(server, username, password):
    auth = lambda data : f'\x00{username}\x00{password}'
    print(f'Authenticating to imaps://{username}:{password}@{server}:993/')
    with imaplib.IMAP4_SSL(server) as conn:
        conn.authenticate('PLAIN', auth)
        conn.noop()
    print('OK')
    print(f'Authenticating to imaps://{username}:{password}@{server}:143/')
    with imaplib.IMAP4(server) as conn:
        conn.starttls()
        conn.authenticate('PLAIN', auth)
        conn.noop()
    print('OK')
    print(f'Authenticating to imap://{username}:{password}@{server}:143/')
    try:
        with imaplib.IMAP4(server) as conn:
            conn.authenticate('PLAIN', auth)
        print(f'Authenticating to imap://{username}:{password}@{server}:143/ worked without STARTTLS!')
        os.exit(102)
    except imaplib.IMAP4.error:
        print('NOK - expected')

def test_pop3(server, username, password):
    print(f'Authenticating to pop3s://{username}:{password}@{server}:995/')
    conn = poplib.POP3_SSL(server)
    conn.capa()
    conn.user(username)
    conn.pass_(password)
    conn.close()
    print('OK')
    print(f'Authenticating to pop3s://{username}:{password}@{server}:110/')
    conn = poplib.POP3(server)
    conn.stls()
    conn.capa()
    conn.user(username)
    conn.pass_(password)
    conn.close()
    print('OK')
    print(f'Authenticating to pop3://{username}:{password}@{server}:110/')
    try:
        conn = poplib.POP3(server)
        conn.capa()
        conn.user(username)
        conn.pass_(password)
        conn.close()
        print(f'Authenticating to pop3://{username}:{password}@{server}:110/ worked without STARTTLS!')
        os.exit(103)
    except poplib.error_proto:
        print('NOK - expected')

def test_SMTP(server, username, password):
    print(f'Authenticating to smtps://{username}:{password}@{server}:465/')
    with smtplib.SMTP_SSL(server) as conn:
        conn.ehlo()
        conn.login(username, password)
        print('OK')
    print(f'Authenticating to smtps://{username}:{password}@{server}:587/')
    with smtplib.SMTP(server, 587) as conn:
        conn.ehlo()
        conn.starttls()
        conn.ehlo()
        conn.login(username, password)
        print('OK')
    try:
        print(f'Authenticating to smtp://{username}:{password}@{server}:587/')
        with smtplib.SMTP(server, 587) as conn:
            conn.ehlo()
            conn.login(username, password)
            print(f'Authenticating to smtp://{username}:{password}@{server}:587/ worked!')
            os.exit(104)
    except smtplib.SMTPNotSupportedError:
        print('NOK - expected')
    #port 25 should fail
    try:
        print(f'Authenticating to smtps://{username}:{password}@{server}:25/')
        with smtplib.SMTP(server) as conn:
            conn.ehlo()
            conn.starttls()
            conn.ehlo()
            conn.login(username, password)
            print(f'Authenticating to smtps://{username}:{password}@{server}:25/ worked!')
            os.exit(105)
    except smtplib.SMTPNotSupportedError:
        print('NOK - expected')
    try:
        print(f'Authenticating to smtp://{username}:{password}@{server}:25/')
        with smtplib.SMTP(server) as conn:
            conn.ehlo()
            conn.login(username, password)
            print(f'Authenticating to smtp://{username}:{password}@{server}:25/ worked without STARTTLS!')
            os.exit(106)
    except smtplib.SMTPNotSupportedError:
        print('NOK - expected')

if __name__ == '__main__':
    test_imap(SERVER, USERNAME, PASSWORD)
    test_pop3(SERVER, USERNAME, PASSWORD)
    test_SMTP(SERVER, USERNAME_ASCII, PASSWORD_ASCII)
#https://github.com/python/cpython/issues/73936
#SMTPlib does not support UTF8 passwords.
