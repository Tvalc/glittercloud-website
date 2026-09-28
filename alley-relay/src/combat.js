import { play } from "./audio.js";
import { WORLD } from "./stages.js";

export function integrate(ent, dt) {
  ent.z += ent.vz * dt;
  ent.vz -= WORLD.gravity * dt;
  if (ent.z <= 0) {
    ent.z = 0;
    if (ent.vz < 0) ent.vz = 0;
  }
  ent.x += ent.vx * dt;
  ent.y += ent.vy * dt;
  if (ent.y < WORLD.floorTop) ent.y = WORLD.floorTop;
  if (ent.y > WORLD.floorBottom) ent.y = WORLD.floorBottom;
}

function hurtbox(ent) {
  return {
    x: ent.x,
    y: ent.y,
    z: ent.z + ent.h * 0.42,
    rx: ent.w * 0.48,
    ry: 24,
    rz: ent.h * 0.46,
  };
}

export function overlaps(hit, ent) {
  const box = hurtbox(ent);
  return (
    Math.abs(hit.x - box.x) < hit.rx + box.rx &&
    Math.abs(hit.y - box.y) < hit.ry + box.ry &&
    Math.abs(hit.z - box.z) < hit.rz + box.rz
  );
}

export function spendSpecial(player) {
  const cost = Math.min(player.fighter.specialCost, Math.max(0, player.hp - 1));
  const red = player.hp - player.chip;
  player.hp -= cost;
  player.chip -= Math.max(0, cost - red);
  if (player.chip < 0) player.chip = 0;
  if (player.chip > player.hp) player.chip = player.hp;
  return cost;
}

export function applyHit(game, spec, target) {
  if (!target || target.state === "dead" || !target.alive) return false;
  if (target.state === "getup" || target.state === "grabbed") return false;
  if (target.team === "player" && target.invuln > 0) return false;

  let dmg = spec.dmg;
  if (target.armor) dmg *= target.armor;
  dmg = Math.max(1, Math.round(dmg));

  const eaten = Math.min(target.chip, dmg);
  target.chip -= eaten;
  target.hp -= eaten;
  let rest = dmg - eaten;
  if (rest > 0) {
    target.hp -= rest;
    target.chip += rest;
  }
  if (target.hp < 0) target.hp = 0;
  target.chip = Math.min(target.chip, target.hp);
  target.chipTimer = 3;
  target.flash = 0.12;

  const facing = spec.radial ? Math.sign(target.x - spec.x) || spec.facing || 1 : spec.facing || 1;
  if (game.attackSlot === target.id) game.attackSlot = null;
  target.vx = facing * spec.kb;
  target.vy = 0;
  if (spec.lift > 50 || target.z > 16) {
    target.state = "air";
    target.vz = Math.max(spec.lift, 90);
  } else {
    target.state = "hurt";
    target.hurtT = 0.42;
    target.vz = 0;
  }
  target.stateT = 0;

  const heavy = spec.kind === "heavy" || spec.kind === "special";
  game.hitstop = Math.max(game.hitstop, spec.hitstop ?? (heavy ? 0.1 : 0.055));
  game.shake = Math.max(game.shake, spec.shake ?? (heavy ? 9 : 5));
  const sparkX = target.x - facing * 16;
  const sparkY = target.y;
  const sparkZ = target.z + 86;
  game.fx.push({
    kind: "spark",
    x: sparkX,
    y: sparkY,
    z: sparkZ,
    t: 0,
    life: 0.14,
    color: spec.team === "player" ? "#ffe7a3" : "#ffb4a2",
    rot: Math.random() * Math.PI,
  });
  game.fx.push({
    kind: "ring",
    x: sparkX,
    y: sparkY,
    z: sparkZ - 10,
    t: 0,
    life: 0.18,
    color: spec.team === "player" ? "#f4efe4" : "#ef6b4a",
  });

  if (spec.team === "player") {
    game.combo += 1;
    game.comboT = 2;
    const base = spec.points ?? 100;
    game.score += Math.round(base * (1 + (game.combo - 1) * 0.25));
    play(spec.kind === "heavy" || spec.kind === "special" ? "heavy" : "hit", game.combo);
  } else {
    play("hurt");
  }

  if (target.hp <= 0) {
    target.hp = 0;
    target.chip = 0;
    target.state = "dead";
    target.alive = false;
    target.deadT = 0.9;
    target.vz = Math.max(target.vz, 220);
    play("ko");
    if (target.team === "enemy") game.score += 500;
    if (target.isBoss) {
      game.banner = `${target.name} is down`;
      game.bannerT = 1.4;
    }
  }
  return true;
}

export function melee(game, owner, spec) {
  const reach = spec.radial ? (spec.reach ?? 40) : Math.max(spec.reach ?? 56, 150);
  const hit = {
    x: spec.radial ? owner.x : owner.x + owner.facing * reach * 0.55,
    y: owner.y,
    z: owner.z + (spec.z ?? 48),
    rx: spec.rx ?? reach * 0.5,
    ry: spec.ry ?? 30,
    rz: spec.rz ?? 40,
    dmg: spec.dmg,
    kb: spec.kb,
    lift: spec.lift ?? 0,
    facing: owner.facing,
    team: owner.team,
    radial: !!spec.radial,
    kind: spec.kind,
    points: spec.points,
    hitstop: spec.hitstop,
    shake: spec.shake,
  };
  const targets = owner.team === "player" ? game.enemies : [game.player];
  let connected = 0;
  for (const target of targets) {
    if (!target || spec.already?.has(target.id)) continue;
    if (!overlaps(hit, target)) continue;
    spec.already?.add(target.id);
    if (applyHit(game, hit, target)) connected += 1;
  }
  return connected;
}

export function updateBody(ent, dt) {
  if (ent.invuln > 0) ent.invuln = Math.max(0, ent.invuln - dt);
  if (ent.flash > 0) ent.flash = Math.max(0, ent.flash - dt);
  if (ent.alive && ent.state !== "dead") {
    if (ent.chipTimer > 0) ent.chipTimer = Math.max(0, ent.chipTimer - dt);
    else if (ent.chip > 0) ent.chip = Math.max(0, ent.chip - 16 * dt);
  }

  if (ent.state === "dead") {
    integrate(ent, dt);
    ent.vx *= Math.exp(-2 * dt);
    ent.deadT -= dt;
    return true;
  }

  if (ent.state === "grabbed") return true;

  if (ent.state === "hurt" || ent.state === "air" || ent.state === "down" || ent.state === "getup") {
    const z0 = ent.z;
    ent.vx *= Math.exp(-2.4 * dt);
    integrate(ent, dt);
    ent.stateT += dt;
    if (ent.state === "air" && z0 > 0 && ent.z === 0) {
      ent.state = "down";
      ent.stateT = 0;
      ent.hurtT = ent.team === "player" ? 0.62 : 0.48;
      ent.vx *= 0.25;
    } else if (ent.state === "hurt" || ent.state === "down" || ent.state === "getup") {
      ent.hurtT -= dt;
      if (ent.hurtT <= 0) {
        if (ent.state === "hurt") ent.state = "idle";
        else if (ent.state === "down") {
          ent.state = "getup";
          ent.hurtT = ent.team === "player" ? 0.34 : 0.26;
          ent.invuln = Math.max(ent.invuln, ent.team === "player" ? 0.85 : 0.32);
        } else {
          ent.state = "idle";
          ent.vx = 0;
          ent.vy = 0;
        }
      }
    }
    return true;
  }

  return false;
}

export function separate(list) {
  for (let i = 0; i < list.length; i += 1) {
    for (let j = i + 1; j < list.length; j += 1) {
      const a = list[i];
      const b = list[j];
      if (!a.alive || !b.alive || a.z > 24 || b.z > 24) continue;
      const depth = Math.abs(a.y - b.y);
      if (depth > 90) continue;
      let dx = b.x - a.x;
      const gap = 66 * ((a.scale || 1) + (b.scale || 1));
      if (Math.abs(dx) >= gap) continue;
      const dir = Math.sign(dx) || 1;
      const push = (gap - Math.abs(dx)) / 2;
      a.x -= dir * push;
      b.x += dir * push;
    }
  }
}
