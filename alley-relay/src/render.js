import { poseFor } from "./fighters.js";
import { drawSprite } from "./sprites.js?v=foe";
import { WORLD } from "./stages.js";

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

export function draw(ctx, game) {
  const cam = game.cameraX || 0;
  const zoom = game.zoom || 1;
  ctx.save();
  if (game.shake > 0.4) {
    ctx.translate((Math.random() - 0.5) * game.shake * 2, (Math.random() - 0.5) * game.shake * 2);
  }
  drawSky(ctx, game);
  ctx.save();
  if (zoom !== 1) {
    ctx.translate(WORLD.viewW / 2, 540);
    ctx.scale(zoom, zoom);
    ctx.translate(-WORLD.viewW / 2, -540);
  }
  drawStreet(ctx, game, cam);
  const sprites = [];
  for (const prop of game.stage?.props || []) {
    sprites.push({ y: prop.y, draw: () => drawProp(ctx, game, prop, cam) });
  }
  for (const pickup of game.stage?.pickups || []) {
    if (pickup.taken) continue;
    sprites.push({ y: pickup.y, draw: () => drawPickup(ctx, pickup, cam) });
  }
  for (const shot of game.projectiles || []) {
    sprites.push({ y: shot.y, draw: () => drawShot(ctx, shot, cam) });
  }
  for (const enemy of game.enemies || []) {
    sprites.push({ y: enemy.y, draw: () => drawPerson(ctx, enemy, cam, game) });
  }
  if (game.player) sprites.push({ y: game.player.y, draw: () => drawPerson(ctx, game.player, cam, game) });
  if (!game.player && (game.mode === "title" || game.mode === "select")) {
    sprites.push({ y: 600, draw: () => drawPerson(ctx, preview("zohran", 280, game), cam, game) });
    sprites.push({ y: 600, draw: () => drawPerson(ctx, preview("abdul", 1000, game), cam, game) });
  }
  sprites.sort((a, b) => a.y - b.y);
  for (const sprite of sprites) sprite.draw();
  for (const fx of game.fx || []) drawFx(ctx, fx, cam);
  drawForeground(ctx, game, cam);
  ctx.restore();
  if (game.mode === "play") drawHud(ctx, game);
  ctx.restore();
}

function preview(id, x, game) {
  const colors = id === "abdul"
    ? { body: "#c4493a", trim: "#7ec8e3", skin: "#d39a6c", pants: "#241c30", bag: "#8d6a45", hat: "tail", sprite: "abdul" }
    : { body: "#3d5a80", trim: "#e2b657", skin: "#e4b48a", pants: "#1c2430", bag: "#c4a574", hat: "cap", sprite: "zohran" };
  return {
    x,
    y: 590,
    z: 0,
    facing: id === "abdul" ? -1 : 1,
    state: "walk",
    stateT: game.time,
    anim: game.time,
    scale: 1,
    team: "player",
    kind: id,
    fighter: { sprite: colors.sprite },
    alive: true,
    isBoss: false,
    flash: 0,
    invuln: 0,
    holding: null,
    name: id,
    colors,
    w: 42,
    h: 88,
  };
}

function drawSky(ctx, game) {
  const stage = game.stage;
  const sky = ctx.createLinearGradient(0, 0, 0, WORLD.viewH);
  sky.addColorStop(0, stage.sky0);
  sky.addColorStop(0.55, stage.sky1);
  sky.addColorStop(1, stage.ground);
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, WORLD.viewW, WORLD.viewH);
}

function tileX(cam, speed, span, index) {
  return index * span - ((cam * speed) % span);
}

function drawStreet(ctx, game, cam) {
  const stage = game.stage;
  const id = stage.id;
  for (let i = -1; i < 10; i += 1) {
    const x = tileX(cam, 0.14, 280, i);
    if (id === "studio") drawStudioFar(ctx, x, i);
    else if (id === "capitol") drawCapitolFar(ctx, x, i);
    else drawRallyFar(ctx, x, i);
  }
  for (let i = -1; i < 8; i += 1) {
    const x = tileX(cam, 0.42, 340, i);
    if (id === "studio") drawStudioMid(ctx, stage, x, i);
    else if (id === "capitol") drawCapitolMid(ctx, stage, x, i);
    else drawRallyMid(ctx, stage, x, i);
  }

  ctx.fillStyle = stage.groundEdge;
  ctx.fillRect(0, WORLD.floorTop - 22, WORLD.viewW, WORLD.viewH - WORLD.floorTop + 22);
  ctx.fillStyle = stage.ground;
  ctx.fillRect(0, WORLD.floorTop, WORLD.viewW, WORLD.floorBottom - WORLD.floorTop + 16);
  ctx.strokeStyle = "rgba(255,255,255,0.07)";
  ctx.lineWidth = 2;
  const groundShift = cam % 90;
  for (let y = WORLD.floorTop + 24; y <= WORLD.floorBottom; y += 40) {
    ctx.beginPath();
    ctx.moveTo(-groundShift, y + (groundShift % 8));
    ctx.lineTo(WORLD.viewW, y);
    ctx.stroke();
  }
  ctx.fillStyle = "rgba(255,255,255,0.04)";
  for (let i = -1; i < 16; i += 1) {
    const x = i * 96 - (cam % 96);
    ctx.fillRect(x, WORLD.floorTop + 70, 28, 4);
  }
}

function drawRallyFar(ctx, x, i) {
  ctx.fillStyle = i % 2 === 0 ? "#1a2230" : "#141b28";
  const h = 90 + (i % 3) * 36;
  ctx.fillRect(x, WORLD.floorTop - h - 40, 160, h);
  if (i % 4 === 0) {
    ctx.fillStyle = "#f4efe4";
    ctx.beginPath();
    ctx.arc(x + 40, 90, 18, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawRallyMid(ctx, stage, x, i) {
  ctx.fillStyle = stage.building;
  ctx.fillRect(x, 168, 230, WORLD.floorTop - 168);
  ctx.fillStyle = stage.trim;
  for (let row = 0; row < 4; row += 1) {
    for (let col = 0; col < 3; col += 1) {
      if ((i + row + col) % 3 === 0) continue;
      ctx.globalAlpha = 0.45;
      ctx.fillRect(x + 22 + col * 64, 190 + row * 46, 26, 16);
      ctx.globalAlpha = 1;
    }
  }
  ctx.fillStyle = stage.accent;
  ctx.fillRect(x + 18, WORLD.floorTop - 46, 120, 16);
}

function drawStudioFar(ctx, x, i) {
  ctx.fillStyle = i % 2 === 0 ? "#241820" : "#1a1218";
  ctx.fillRect(x, 80, 200, WORLD.floorTop - 120);
  ctx.fillStyle = i % 3 === 0 ? "#8fd0ff" : "#e23b4a";
  ctx.globalAlpha = 0.55;
  ctx.fillRect(x + 30, 140, 70, 40);
  ctx.globalAlpha = 1;
}

function drawStudioMid(ctx, stage, x, i) {
  ctx.fillStyle = stage.building;
  ctx.fillRect(x, 150, 250, WORLD.floorTop - 150);
  ctx.fillStyle = stage.trim;
  ctx.fillRect(x + 16, 170, 210, 8);
  ctx.fillStyle = "#1a120f";
  ctx.fillRect(x + 40, 200, 150, 90);
  ctx.fillStyle = i % 2 === 0 ? "#8fd0ff" : "#f0c14a";
  ctx.globalAlpha = 0.35;
  ctx.fillRect(x + 52, 214, 126, 62);
  ctx.globalAlpha = 1;
}

function drawCapitolFar(ctx, x, i) {
  ctx.fillStyle = "#243044";
  ctx.fillRect(x, 160, 90, WORLD.floorTop - 200);
  if (i % 3 === 1) {
    ctx.beginPath();
    ctx.arc(x + 46, 160, 48, Math.PI, 0);
    ctx.fill();
  }
}

function drawCapitolMid(ctx, stage, x, i) {
  ctx.fillStyle = stage.building;
  ctx.fillRect(x, 140, 250, WORLD.floorTop - 140);
  ctx.fillStyle = stage.trim;
  for (let col = 0; col < 4; col += 1) {
    ctx.fillRect(x + 28 + col * 52, 168, 18, WORLD.floorTop - 190);
  }
  ctx.fillRect(x, 156, 250, 14);
}

function drawForeground(ctx, game, cam) {
  const id = game.stage?.id;
  ctx.save();
  for (let i = -1; i < 12; i += 1) {
    const x = tileX(cam, 1.22, 180, i);
    if (id === "studio") {
      ctx.fillStyle = "rgba(18,10,8,0.55)";
      ctx.fillRect(x, 690, 140, 30);
      ctx.fillStyle = "rgba(240,193,74,0.35)";
      ctx.fillRect(x + 8, 686, 40, 6);
    } else if (id === "capitol") {
      ctx.strokeStyle = "rgba(210,214,220,0.45)";
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(x, 700);
      ctx.lineTo(x + 150, 688);
      ctx.stroke();
      ctx.fillStyle = "rgba(180,186,196,0.5)";
      ctx.fillRect(x, 688, 6, 32);
    } else {
      ctx.fillStyle = "rgba(20,16,14,0.5)";
      ctx.fillRect(x, 692, 110, 22);
      ctx.fillStyle = "rgba(224,164,90,0.45)";
      ctx.fillRect(x + 8, 684, 18, 14);
    }
  }
  ctx.restore();
}

function drawProp(ctx, game, prop, cam) {
  const x = prop.x - cam;
  const y = prop.y;
  ctx.fillStyle = "rgba(0,0,0,0.25)";
  ctx.fillRect(x - prop.w / 2, y - 8, prop.w, 10);
  if (game.stage.id === "studio") {
    ctx.fillStyle = "#6b4634";
    ctx.fillRect(x - prop.w / 2, y - prop.h, prop.w, prop.h);
    ctx.fillStyle = game.stage.accent;
    ctx.fillRect(x - prop.w / 2 - 8, y - prop.h - 10, prop.w + 16, 12);
  } else if (game.stage.id === "capitol") {
    ctx.fillStyle = "#3d4654";
    ctx.fillRect(x - prop.w / 2, y - prop.h, prop.w, prop.h);
    ctx.fillStyle = game.stage.accent;
    ctx.fillRect(x - 6, y - prop.h - 16, 12, 18);
  } else {
    ctx.fillStyle = "#6d5834";
    ctx.fillRect(x - prop.w / 2, y - prop.h, prop.w, prop.h);
    ctx.strokeStyle = "rgba(0,0,0,0.25)";
    ctx.strokeRect(x - prop.w / 2, y - prop.h, prop.w, prop.h);
  }
}

function drawPickup(ctx, pickup, cam) {
  const x = pickup.x - cam;
  const y = pickup.y;
  ctx.fillStyle = "rgba(0,0,0,0.3)";
  ctx.beginPath();
  ctx.ellipse(x, y, 16, 6, 0, 0, Math.PI * 2);
  ctx.fill();
  if (pickup.kind === "pipe") {
    ctx.strokeStyle = "#d9dde6";
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(x - 16, y - 8);
    ctx.lineTo(x + 16, y - 20);
    ctx.stroke();
  } else {
    ctx.fillStyle = "#d7e7a0";
    roundRect(ctx, x - 5, y - 22, 10, 18, 3);
    ctx.fill();
  }
}

function drawShot(ctx, shot, cam) {
  const x = shot.x - cam;
  const y = shot.y - shot.z;
  ctx.save();
  ctx.translate(x, y);
  if (shot.kind === "bolt") {
    const dir = Math.sign(shot.vx) || 1;
    ctx.fillStyle = "rgba(90, 186, 255, 0.35)";
    ctx.beginPath();
    ctx.ellipse(-dir * 16, 0, 26, 9, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#6ec0ff";
    ctx.beginPath();
    ctx.arc(0, 0, 12, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#f4fbff";
    ctx.beginPath();
    ctx.arc(-dir * 2, -1, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    return;
  }
  ctx.rotate(shot.spin);
  if (shot.kind === "pipe") {
    ctx.strokeStyle = "#e8eef8";
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(-16, 0);
    ctx.lineTo(16, 0);
    ctx.stroke();
  } else {
    ctx.fillStyle = "#d7e7a0";
    ctx.fillRect(-4, -8, 8, 16);
  }
  ctx.restore();
}

function drawFx(ctx, fx, cam) {
  const alpha = 1 - fx.t / fx.life;
  const x = fx.x - cam;
  const y = fx.y - fx.z;
  ctx.save();
  ctx.globalAlpha = Math.max(0, alpha);
  if (fx.kind === "spark") {
    ctx.translate(x, y);
    ctx.rotate(fx.rot || 0);
    ctx.strokeStyle = fx.color;
    ctx.lineWidth = 3;
    for (let i = 0; i < 6; i += 1) {
      const a = (i / 6) * Math.PI * 2;
      const len = 10 + fx.t * 90;
      ctx.beginPath();
      ctx.moveTo(Math.cos(a) * 4, Math.sin(a) * 4);
      ctx.lineTo(Math.cos(a) * len, Math.sin(a) * len);
      ctx.stroke();
    }
  } else if (fx.kind === "dust") {
    ctx.fillStyle = fx.color;
    ctx.beginPath();
    ctx.ellipse(x, y - fx.t * 18, 8 + fx.t * 28, 4 + fx.t * 8, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.fillStyle = fx.color;
    ctx.beginPath();
    ctx.arc(x, y, 6 + fx.t * 28, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

function drawPerson(ctx, ent, cam, game) {
  if (ent.team === "player" && ent.invuln > 0 && Math.floor(game.time * 16) % 2 === 0 && ent.state !== "special") return;
  const depth = 0.86 + ((ent.y - WORLD.floorTop) / (WORLD.floorBottom - WORLD.floorTop)) * 0.2;
  const sc = (ent.scale || 1) * depth;
  const sx = ent.x - cam;
  const colors = ent.colors;
  const pose = poseFor(ent);
  const flash = ent.flash > 0;
  const spriteScale = sc * 1.05;

  ctx.save();
  ctx.translate(sx, ent.y);
  ctx.scale(spriteScale, spriteScale * 0.42);
  ctx.fillStyle = "rgba(0,0,0,0.35)";
  ctx.beginPath();
  ctx.ellipse(0, 8, 54, 18, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  if (drawSprite(ctx, ent, sx, spriteScale)) {
    label(ctx, ent, sx);
    return;
  }

  ctx.save();
  ctx.translate(sx, ent.y);
  ctx.scale(sc, sc * 0.42);
  ctx.fillStyle = "rgba(0,0,0,0.35)";
  ctx.beginPath();
  ctx.ellipse(0, 0, 26, 18, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  ctx.save();
  ctx.translate(sx, ent.y - ent.z);
  ctx.scale(sc * (ent.facing || 1), sc);
  const ink = flash ? "#ffffff" : null;
  if (pose.down) {
    ctx.fillStyle = ink || colors.pants;
    ctx.fillRect(-36, -18, 54, 14);
    ctx.fillStyle = ink || colors.body;
    ctx.fillRect(-8, -24, 34, 16);
    ctx.fillStyle = ink || colors.skin;
    ctx.beginPath();
    ctx.arc(30, -20, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    label(ctx, ent, sx);
    return;
  }

  const step = pose.step || 0;
  const lean = pose.lean || 0;
  ctx.fillStyle = ink || colors.pants;
  ctx.fillRect(-12, -40, 9, 36 + step * 2);
  ctx.fillRect(2, -40, 9, 36 - step * 2);
  ctx.fillStyle = ink || colors.skin;
  ctx.fillRect(-14, -44, 8, 8);
  ctx.fillRect(6, -44, 8, 8);

  ctx.fillStyle = ink || colors.body;
  ctx.fillRect(-16 + lean * 0.2, -78, 32, 42);
  ctx.fillStyle = ink || colors.trim;
  ctx.fillRect(-16 + lean * 0.2, -62, 32, 7);

  if (ent.team === "player" && colors.bag) {
    ctx.fillStyle = ink || colors.bag;
    ctx.fillRect(-20, -70, 8, 16);
  }

  ctx.fillStyle = ink || colors.skin;
  ctx.beginPath();
  ctx.arc(lean * 0.15, -92, 14, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = ink || colors.trim;
  if (colors.hat === "cap") ctx.fillRect(-15, -106, 30, 8);
  if (colors.hat === "helm") {
    ctx.beginPath();
    ctx.arc(0, -96, 16, Math.PI, 0);
    ctx.fill();
  }
  if (colors.hat === "tail") ctx.fillRect(-26, -96, 18, 5);

  const punch = pose.punch || 0;
  ctx.fillStyle = ink || colors.skin;
  ctx.fillRect(-20, -70, 10, 8);
  ctx.fillStyle = ink || colors.body;
  ctx.fillRect(8, -70 - punch * 4, 12 + punch * 36, 8);

  if (ent.holding?.kind === "pipe" && !pose.down) {
    ctx.strokeStyle = "#e8eef8";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(16 + punch * 20, -78);
    ctx.lineTo(36 + punch * 28, -92);
    ctx.stroke();
  } else if (ent.holding?.kind === "bottle") {
    ctx.fillStyle = "#d7e7a0";
    ctx.fillRect(18, -86, 7, 14);
  }

  if (pose.special) {
    ctx.globalAlpha = 0.35;
    ctx.fillStyle = colors.trim;
    ctx.beginPath();
    ctx.arc(0, -50, 70, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
  }
  ctx.restore();
  label(ctx, ent, sx);
}

function label(ctx, ent, sx) {
  if (!ent.isBoss || !ent.alive) return;
  ctx.fillStyle = "#f4efe4";
  ctx.font = "700 16px Segoe UI, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(ent.name, sx, ent.y - ent.z - (ent.h || 90) * (ent.scale || 1) - 16);
}

function drawHud(ctx, game) {
  const player = game.player;
  if (!player) return;
  ctx.textAlign = "left";
  ctx.font = "700 18px Segoe UI, sans-serif";
  ctx.fillStyle = "#f4efe4";
  ctx.fillText(player.name, 36, 40);
  bar(ctx, 36, 52, 280, 16, player);

  ctx.font = "600 14px Segoe UI, sans-serif";
  ctx.fillStyle = "#e2b657";
  ctx.fillText(`Lives ${game.lives}`, 36, 92);

  ctx.textAlign = "right";
  ctx.fillStyle = "#f4efe4";
  ctx.font = "700 20px Segoe UI, sans-serif";
  ctx.fillText(String(game.score).padStart(6, "0"), WORLD.viewW - 36, 42);
  if (game.combo >= 2) {
    ctx.fillStyle = "#ef6b4a";
    ctx.font = "800 28px Segoe UI, sans-serif";
    ctx.fillText(`${game.combo} HITS`, WORLD.viewW - 36, 78);
  }

  const boss = (game.enemies || []).find((enemy) => enemy.isBoss && enemy.alive);
  if (boss) {
    ctx.textAlign = "center";
    ctx.fillStyle = "#f4efe4";
    ctx.font = "700 16px Segoe UI, sans-serif";
    ctx.fillText(boss.name, WORLD.viewW / 2, 36);
    bar(ctx, WORLD.viewW / 2 - 160, 46, 320, 14, boss);
  }

  if (player.holding) {
    ctx.textAlign = "left";
    ctx.fillStyle = "#f4efe4";
    ctx.font = "700 16px Segoe UI, sans-serif";
    const word = player.holding.kind === "pipe" ? `Pipe ${player.holding.left}` : "Bottle";
    ctx.fillText(word, 36, WORLD.viewH - 36);
  }

  if (game.banner && (game.bannerT > 0 || game.introT > 0)) {
    ctx.textAlign = "center";
    ctx.fillStyle = "#f4efe4";
    ctx.font = "800 42px Segoe UI, sans-serif";
    ctx.fillText(game.banner, WORLD.viewW / 2, 150);
    if (game.introT > 0.2 && game.stage?.line) {
      ctx.font = "600 18px Segoe UI, sans-serif";
      ctx.fillStyle = "#e2b657";
      ctx.fillText(game.stage.line, WORLD.viewW / 2, 184);
    }
  }
}

function bar(ctx, x, y, w, h, ent) {
  const red = Math.max(0, ent.hp - ent.chip) / ent.hpMax;
  const green = Math.max(0, ent.chip) / ent.hpMax;
  ctx.fillStyle = "rgba(0,0,0,0.45)";
  ctx.fillRect(x, y, w, h);
  ctx.fillStyle = "#d24b3a";
  ctx.fillRect(x, y, w * Math.min(1, red), h);
  ctx.fillStyle = "#7dce6a";
  ctx.fillRect(x + w * Math.min(1, red), y, w * Math.min(1 - red, green), h);
  ctx.strokeStyle = "rgba(244,239,228,0.7)";
  ctx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
}
