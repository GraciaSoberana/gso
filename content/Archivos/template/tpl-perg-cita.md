<grid drag="100 75" drop="0 3" style="display:flex;flex-direction:column;align-items:center;justify-content:space-around;text-align:center;padding:3% 0;">

<div class="perg-dia-wrap">
  <div class="perg-dia-line"></div>
  <span class="perg-dia"><% dia %></span>
  <div class="perg-dia-line"></div>
</div>

<div style="display:flex;flex-direction:column;align-items:center;width:100%;">
  <div class="perg-versiculo-texto"><% cita %></div>
  <div class="perg-autor"><% autor %></div>
  <div class="perg-libro"><%? libro %></div>
</div>

<% content %>

</grid>

<grid drag="30 18" drop="35 79">
<img src="./css/logo-redes.svg" class="perg-logo" style="width:100%;" />
</grid>
