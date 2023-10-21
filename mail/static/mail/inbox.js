document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  const composeBtn = document.querySelector('#compose-btn');

  composeBtn.addEventListener('click', (e) => {
    e.preventDefault();
  
    document.getElementById("compose-errors").innerHTML = '';
  
    fetch("/emails", {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(response => {
      if (response.error) {
        document.getElementById("compose-errors").innerHTML = `
          <div class="alert alert-danger">${response.error}</div>
        `;
  
        return;
      }
  
      load_mailbox('sent')
    })
    .catch(error => {
      document.getElementById("compose-errors").innerHTML = `
          <div class="alert alert-danger">There was a server error, please try again</div>
      `;
    })
  });
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {
    for(const mail of data) {
      const card = document.createElement('div');
      card.classList.add('card');
      card.style.backgroundColor = mail.read ? 'white' : 'gray'; 
      card.style.width = '18rem';
      card.style.marginBottom = '15px';
      
      const cardBody = document.createElement('div');
      cardBody.classList.add('card-body');

      const subjectHeading = document.createElement('h5');
      subjectHeading.classList.add('card-title');
      subjectHeading.textContent = mail.subject;

      const senderParagraph = document.createElement('p');
      senderParagraph.classList.add('card-text');
      senderParagraph.textContent = mail.sender;

      const timestampParagraph = document.createElement('p');
      timestampParagraph.textContent = mail.timestamp;

      const readButton = document.createElement('button');
      readButton.classList.add('btn');
      readButton.classList.add('btn-primary');
      readButton.textContent = 'Read';
      readButton.addEventListener('click', () => load_mail(mail.id, mailbox));

      cardBody.appendChild(subjectHeading);
      cardBody.appendChild(senderParagraph);
      cardBody.appendChild(timestampParagraph);
      cardBody.appendChild(readButton);

      if(mailbox === 'inbox') {
        const archiveButton = document.createElement('button');
        archiveButton.classList.add('btn');
        archiveButton.classList.add('btn-secondary');
        archiveButton.textContent = 'Archive'
        archiveButton.style.marginLeft = '10px';
        archiveButton.addEventListener('click', () => archive(mail.id));

        cardBody.appendChild(archiveButton);
      }

      if (mailbox === 'archive') {
        const unarchiveButton = document.createElement('button');
        unarchiveButton.classList.add('btn');
        unarchiveButton.classList.add('btn-secondary');
        unarchiveButton.textContent = 'Unarchive'
        unarchiveButton.style.marginLeft = '10px';
        unarchiveButton.addEventListener('click', () => unarchive(mail.id));

        cardBody.appendChild(unarchiveButton);
      }

      card.appendChild(cardBody);
      document.querySelector('#emails-view').appendChild(card);
    }
  })
}

function load_mail(id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'block';

  document.querySelector('#read-view-content').innerHTML = '';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(data => {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })

    // create elements
    const topParagraphFontSize = '1.4rem';
    const senderParagraph = document.createElement('p');
    const recipientsParagraph = document.createElement('p');
    const subjectParagraph = document.createElement('p');
    const timestampParagraph = document.createElement('p');
    const bodyParagraph = document.createElement('p');

    // add styling to the elements
    senderParagraph.style.fontSize = topParagraphFontSize;
    recipientsParagraph.style.fontSize = topParagraphFontSize;
    subjectParagraph.style.fontSize = topParagraphFontSize;
    timestampParagraph.style.fontSize = topParagraphFontSize;
    bodyParagraph.style.fontSize = '1.2rem';
    
    // add content to the elements
    senderParagraph.textContent = `Sender: ${data.sender}`;
    recipientsParagraph.textContent = `Recipients: ${data.recipients.join(', ')}`;
    subjectParagraph.textContent = `Subject: ${data.subject}`;
    timestampParagraph.textContent = `Timestamp: ${data.timestamp}`;
    bodyParagraph.textContent = data.body;

    // add the elements to the appropriate element
    document.querySelector('#read-view-content').appendChild(senderParagraph);
    document.querySelector('#read-view-content').appendChild(recipientsParagraph);
    document.querySelector('#read-view-content').appendChild(subjectParagraph);
    document.querySelector('#read-view-content').appendChild(timestampParagraph);
    document.querySelector('#read-view-content').appendChild(bodyParagraph);

    if (mailbox === 'inbox') {
      const replyButton = document.createElement('button');
      replyButton.classList.add('btn');
      replyButton.classList.add('btn-secondary');
      replyButton.textContent = 'Reply'
      replyButton.addEventListener('click', () => reply(data));

      document.querySelector('#read-view-content').appendChild(replyButton);
    }
  });
}

function reply(mail) {
  compose_email();

  document.querySelector('#compose-recipients').value = mail.sender;
  document.querySelector('#compose-subject').value = mail.subject.includes('Re: ') ? mail.subject : `Re: ${mail.subject}`;
  document.querySelector('#compose-body').value = `On ${mail.timestamp} ${mail.sender} wrote: ${mail.body}`;
}

function archive(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  .then(response => load_mailbox('inbox'));
}

function unarchive(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  .then(response => load_mailbox('inbox'));;
}