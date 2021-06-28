import sys
from distutils.util import strtobool
import glob
import os
from datetime import date
import smtplib
from email.message import EmailMessage


import numpy as np
import pandas as pd
from enviro import GMAIL_LOGIN, GMAIL_PWD, MESSAGE_how_to, MESSAGE_solution, PROJECT_PATH


PATH = PROJECT_PATH


def get_notebook_to_send(row, df, PATH):
    """Find the first empty column and return dict of some row values.
    Args
    ----
        row: pandas.core.series.Series
        df:  pandas.core.frame.DataFrame
        PATH: str, path to notebooks
    Returns
    -------
        d: dict, dictionary of data for given row at first empty column
    """
    for idx, col in enumerate(row):
        try:
            if np.isnan(col):
                d = {'name': row.recipient,
                     'email': row.email,
                     'challenge': df.columns[idx],
                     'challenge_path': PATH + df.columns[idx],
                    }
                return d
        except TypeError:
            continue


def send_email(challenge,
               path,
               recipient,
               msg_to,
               msg_from='robert@agilescientific.com',
               dry_run=True):
    """Send jupyter notebook to student.
    Args
    ----
        challenge: str, challenge filename
        path: str, path to notebooks, example: './weekly-challenge/notebooks/'
        recipient: str, name of the recipient
        msg_to: str, email of the recipient
        msg_from: str, email to show as sender
        dry_run: bool, no emails sent if True
    Returns
    -------
        None
    """
    # create message object and initialize variables
    msg            = EmailMessage()
    msg['From']    = msg_from
    msg['To']      = msg_to

    # Adjustments depending on challenge_name
    if challenge == 'How_to_use_these_kata.ipynb':
        msg['Subject'] = 'How to use the Agile Katas'
        msg.set_content(MESSAGE_how_to.format(recipient))
    else:
        challenge_name = challenge.replace('_solution.ipynb', '')
        msg['Subject'] = f'Agile Katas solution for {challenge_name}'
        msg.set_content(MESSAGE_solution.format(recipient, challenge_name))

    # read the jupyter notebook
    with open(f'{path}{challenge}', 'rb') as f:
        notebook_data = f.read()

    # add attachment
    msg.add_attachment(notebook_data, maintype='text', subtype='ipynb', filename=challenge)

    # send email
    if dry_run:
            print(f'>>> Dry run: would have sent {challenge} to {recipient} @ {msg_to} <<<')
    else:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            print(f'>>> Sending {challenge} to {recipient} @ {msg_to} <<<')
            smtp.login(GMAIL_LOGIN, GMAIL_PWD)
            assert msg['To'] == msg_to
            # ************** WARNING *************
            # the next line sends the actual email
            smtp.send_message(msg)

    # logging
    print(f'*** On {date.today()}, {challenge} was sent to {msg_to} ***\n')

    return None


def send_summary_email(notebooks_sent,
                       n,
                       msg_to='robert@agilescientific.com',
                       msg_from='robert@agilescientific.com',
                       dry_run=True):
    """Send a summary email including which files were sent to who.
    Args
    ----
        notebooks_sent: dict, k is notebooks and v is list of recipients
        n: int, number of emails sent
        dry_run: bool, no email sent if True
    Returns
    -------
        None
    """
    msg            = EmailMessage()
    msg['From']    = msg_from
    msg['To']      = msg_to
    msg['Subject'] = f'Kata summary email for {date.today().isoformat()}'
    message = 'Summary kata email for {}:\n\n{}\n{} notebooks sent in total.'
    lines = ''
    for k, v in notebooks_sent.items():
        lines += f'{k} sent to:\n{v}\n'
    msg.set_content(message.format(date.today(), lines, n))

    if dry_run:
        print(f'\nDry run: Would have sent summary email to {msg_to} with msg:\n{"-"*40}\n{msg}\n{"-"*40}')
    else:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_LOGIN, GMAIL_PWD)
            print(f'Sending summary email to {msg_to}')
            assert msg['To'] == msg_to
            # ************** WARNING *************
            # the next line sends the actual email
            smtp.send_message(msg)

    return None


def iterate_and_send(fname, dry_run=True):
    """Load the tracking CSV file and send emails as required."""
    # variables
    global PATH

    df             = pd.read_csv(fname)
    n              = 0
    challenges     = []
    notebooks_sent = {}
    for col in df.columns[4:]:
        notebooks_sent[col] = []

    # iterate
    for row, d in enumerate(df.apply(get_notebook_to_send, axis=1, args=(df, PATH))):
        # skip if solution already sent
        if d is None:
            continue
        else:
            if d['challenge'] not in challenges:
                challenges.append(d['challenge'])
            col = d['challenge']
            # send email and log progress
            send_email(d['challenge'], PATH, d['name'], d['email'], dry_run=dry_run)
            notebooks_sent[d['challenge']].append(d['email'])
            n += 1
            df.loc[row, col] = date.today().isoformat()
            # write to local file
            if not dry_run:
                df.to_csv(fname, index=False)

    print(f'Logging...:\nEmailing complete, {n} emails sent.')
    print(f'{n} updates to \'{fname}\' done on {date.today()}\n')

    # email summary
    if n > 0:
        notebooks_sent = {k: v for k, v in notebooks_sent.items() if v}
        send_summary_email(notebooks_sent, n, dry_run=dry_run)

    return df


def main(fname, dry_run):
    _ = iterate_and_send(fname, dry_run=dry_run)

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        msg = 'No file name given, you must pass the fname of the target CSV containing email recipients'
        raise IndexError(msg)
    try:
        dry_run = bool(strtobool(sys.argv[2]))
    except IndexError:
        dry_run = True
    main(fname, dry_run)
