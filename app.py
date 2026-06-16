<!-- واجهة الشحن -->
<div id="charge-box">
    <h3>شحن الكريستال - Bot al-Sabaa</h3>
    <input type="text" id="playerId" placeholder="أدخل رمز المستخدم الخاص بك">
    <input type="number" id="amount" placeholder="كمية الكريستال">
    <button onclick="sendChargeRequest()">تأكيد الشحن</button>
</div>

<script>
function sendChargeRequest() {
    const pId = document.getElementById('playerId').value;
    const qty = document.getElementById('amount').value;
    
    // رابط السيرفر الخاص بك على Railway
    const serverUrl = "https://your-app-name.up.railway.app/api/charge"; 

    fetch(serverUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            playerId: pId,
            amount: parseInt(qty),
            secretKey: "YOUR_SECRET_KEY" // هذا المفتاح السري الذي وضعته في إعدادات السيرفر
        })
    })
    .then(response => response.json())
    .then(data => {
        alert("تم إرسال طلب الشحن بنجاح!");
    })
    .catch(error => {
        alert("حدث خطأ، تأكد من اتصالك بالسيرفر");
    });
}
</script>
