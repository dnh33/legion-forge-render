# legion-forge-render

A free, public image pipeline for the art in [Legion](https://github.com/dnh33/legion)'s War Room: painted half-length portraits of the 13 offices and the hero backdrops ("vistas") for every theme and Depth.

- **Model:** FLUX.1-schnell by Black Forest Labs, Apache-2.0, as a Q4_K_S GGUF ([city96](https://huggingface.co/city96/FLUX.1-schnell-gguf)).
- **Runtime:** [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) (MIT), CPU only, on GitHub-hosted runners (free for public repositories).
- **Prompts:** `prompts/busts.json`, `prompts/vistas.json`. One shared style block per set, one line per item, fixed seeds.
- **Output:** the `renders` branch (PNG + JSON metadata per image, contact sheets in `renders/sheets/`) and the run's artifacts.

## Run it

Actions → *Render reliquaries and vistas* → Run workflow. Choose a set, optionally a comma-separated list of ids, and the number of seeds per item.

## Runners

`ubuntu-latest` (4 vCPU, 16 GB RAM for public repos) is the default and the one that fits the models in memory. The macOS arm64 runners (3 vCPU M1, 7 GB RAM) cannot use the Apple GPU from inside the VM, so they run on CPU with less memory than the models need; they are offered as an experiment only. For speed, the same prompts run locally in ComfyUI on an RTX-class GPU.

## Rules for the art

Grimdark, sincere and maximal, in original designs. Genre tropes are in: hooded machine-acolytes, robes over augmetics, glowing optics, mechanical arms, wax seals, censers, skulls as memento mori, forge-cathedrals. Other people's marks are out: no two-headed birds or eagles, no skull-in-a-cog emblem, no floating skull drones, no power-armour soldiers or pauldrons, no franchise names or text.
