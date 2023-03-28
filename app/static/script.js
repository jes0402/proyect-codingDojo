function showMessage() {
    var status = document.createElement('span');
    status.innerHTML = 'Preparing your order...';
    event.target.parentNode.appendChild(status);
    }