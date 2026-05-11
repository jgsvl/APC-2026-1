// Create your variables here
var score = 0;
var xNave = 200;
var yNave = 350;
// Create your sprites here
var fundo = createSprite(200, 200);
fundo.setAnimation("fundo");

var tiro = createSprite(xNave, yNave+10);
tiro.setAnimation("tiro");

var nave = createSprite(xNave, yNave);
nave.setAnimation("nave");

var alien = createSprite(randomNumber(50, 350),-50);
alien.scale = .15;
alien.setAnimation("alien");

function draw() {
  background("darkorchid");
  alien.velocityY = 8;
  nave.velocityX = 0;
  tiro.velocityX = 0;
  if (keyDown("left")){
    nave.velocityX = -5;
    if (tiro.y >= yNave){
      tiro.velocityX = -5;
    }
  }
    if (keyDown("right")){
    nave.velocityX = 5;
    if(tiro.y >= yNave){
      tiro.velocityX = 5;  
    }
    
  }
  if (tiro.y < 0){
    resetTiro();
  }
  if(keyDown("space")){
    tiro.velocityY = -15;
  }
  
  if(tiro.collide(alien)){
    score+=1;
    resetTiro();
    resetAlien();
  }
  if (alien.y > 400){
    score -= 1;
    resetAlien();
  }
  
  if (alien.collide(nave)){
    resetAlien();
    score-=2;
  }

  drawSprites();
  textSize(20);
  text("Score: " + score, 10, 10, 100, 100);
  
}

function resetAlien(){
  alien.y = -50;
  alien.x = randomNumber(50, 350);
}

function resetTiro(){
    tiro.y = nave.y+10;
    tiro.x = nave.x;
    tiro.velocityY = 0;
}