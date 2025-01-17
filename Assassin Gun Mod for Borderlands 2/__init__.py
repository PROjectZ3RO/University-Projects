'''
NOTE: This file is a Work in Progress as I learn to incorporate game files into this code

I am currently trying to fix the magazine size to 1 but this is proving more difficult because of the effects (skills and class mods)
that increase magazine size for guns
'''

import bl2sdk
import random

class Assassin(bl2sdk.BL2MOD):
    Name = "Assassin Gun"
    Description = "Replaces the Skullmasher with Assassin, a sniper Rifle that slows down time while aiming down sights and grants massive crit damage."
    Author = "PRO(ject)Z3R0" 

    def part_changes(self):
            # Find the specific weapon parts for the Skullmasher
            AssassinBarrel = bl2sdk.FindObject("WeaponPartDefinition", "GD_Weap_SniperRifles.Barrel.SR_Barrel_Jakobs_Skullmasher")
            AssassinTitle = bl2sdk.FindObject("WeaponNamePartDefinition", "GD_Weap_SniperRifles.Name.Title_Jakobs.Title_Legendary_Skullmasher")
            AssassinRedText = bl2sdk.FindObject("AttributePresentationDefinition", "GD_Weap_SniperRifles.Name.Title_Jakobs.Title_Legendary_Skullmasher:AttributePresentationDefinition_8")

            # Change the name and red text
            AssassinTitle.PartName = "Assassin"
            AssassinRedText.NoConstraintText = "It won't take more than one shot"

            # Find the relevant attribute definitions
            ClipSize = bl2sdk.FindObject("AttributeDefinition", "D_Attributes.Weapon.WeaponClipSize")
            CritDamage = bl2sdk.FindObject("AttributeDefinition", "D_Attributes.GameplayAttributes.PlayerCriticalHitBonus")

            # Ensure AssassinBarrel.WeaponAttributeEffects has enough slots, extend if necessary
            required_slots = 4  # Number of effects we need to set
            if len(AssassinBarrel.WeaponAttributeEffects) < required_slots:
                for _ in range(required_slots - len(AssassinBarrel.WeaponAttributeEffects)):
                    AssassinBarrel.WeaponAttributeEffects.append(bl2sdk.FAttributeEffect())

            # Clear existing attribute effects to prevent conflicts
            for effect in AssassinBarrel.WeaponAttributeEffects:
                effect.AttributeToModify = None
                effect.ModifierType = 0
                effect.BaseModifierValue.BaseValueConstant = 0.0

            # Set the magazine size to 1 using MT_Scale
            AssassinBarrel.WeaponAttributeEffects[0].AttributeToModify = ClipSize
            AssassinBarrel.WeaponAttributeEffects[0].ModifierType = 0  # MT_Scale
            AssassinBarrel.WeaponAttributeEffects[0].BaseModifierValue.BaseValueConstant = 1.0

            # Increase critical hit damage by 10000.0%
            AssassinBarrel.WeaponAttributeEffects[1].AttributeToModify = CritDamage
            AssassinBarrel.WeaponAttributeEffects[1].ModifierType = 0  # MT_Scale
            AssassinBarrel.WeaponAttributeEffects[1].BaseModifierValue.BaseValueConstant = 10000.0

            # Log confirmation
            bl2sdk.Log("Assassin Gun: Magazine size set to 1 and critical hit damage increased by 10000.0%")


    def get_player_controller(self):
        return bl2sdk.GetEngine().GamePlayers[0].Actor


    # This function contains a list of all Sniper skins in the game, its used to randomly chose any of these skins as a template for Assassin Skin.
    def get_random_skin(self):
        SniperSkins = [
            "Aster_GunMaterials.Materials.sniper.Mati_Dahl_Emerald_Sniper",
            "Aster_GunMaterials.Materials.sniper.Mati_Hyperion_Diamond_Sniper",
            "Aster_GunMaterials.Materials.sniper.Mati_Jakobs_Citrine_Sniper",
            "Aster_GunMaterials.Materials.sniper.Mati_Maliwan_Aquamarine_Sniper",
            "Aster_GunMaterials.Materials.sniper.Mati_Vladof_Garnet_Sniper",
            "Common_GunMaterials.Materials.sniper.Mati_GearboxSR",
            "Common_GunMaterials.Materials.sniper.Mati_HyperionUniqueSR_Morningstar",
            "Common_GunMaterials.Materials.sniper.Mati_JakobsUniqueSR_Tresspasser",
            "Common_GunMaterials.Materials.sniper.Mati_MaliwanEpicSR",
            "Common_GunMaterials.Materials.sniper.Mati_MaliwanLegendarySRVolcano",
            "Common_GunMaterials.Materials.sniper.Mati_MaliwanRareSR",
            "Common_GunMaterials.Materials.sniper.Mati_MaliwanUniqueSR_ChereAmie",
            "Gladiolus_GunMaterials.Materials.sniper.Mati_Maliwan_6_Storm",
            "Iris_GunMaterials.Materials.sniper.Mati_JakobsUniqueSR_Cobra",
        ]
        return random.choice(SniperSkins)


    '''
    This function gets called every time the player unzooms the chronos, it will then randomly change the weapons skin
    It uses one random already existing sniper skin as a template. It copies all the values from the template to its own skin.
    '''
    # Search first for the Material of the Skullmasher
    AssassinMaterial = bl2sdk.FindObject("MaterialInstanceConstant", "Common_GunMaterials.Materials.sniper.Mati_JakobsLegendarySRSkullmasher")
    
    def randomize_weapon_skin(self):
        
        # Find the MaterialInstanceConstant of Random Skin
        RandomMaterial = bl2sdk.FindObject("MaterialInstanceConstant", self.get_random_skin())

        # Some skins use a parent skin as a template, in that case copy its values first!
        if not RandomMaterial.Parent.Name == "Master_Gun":
            for temp in RandomMaterial.Parent.VectorParameterValues:
                color = (temp.ParameterValue.R, temp.ParameterValue.G, temp.ParameterValue.B, temp.ParameterValue.A)
                self.AssassinMaterial.SetVectorParameterValue(temp.ParameterName, color)
            for temp in RandomMaterial.Parent.TextureParameterValues:
                if not temp.ParameterValue is None:
                    self.AssassinMaterial.SetTextureParameterValue(temp.ParameterName, temp.ParameterValue)
            for temp in RandomMaterial.Parent.ScalarParameterValues:
                self.AssassinMaterial.SetScalarParameterValue(temp.ParameterName, temp.ParameterValue)

        for temp in RandomMaterial.VectorParameterValues:
            color = (temp.ParameterValue.R, temp.ParameterValue.G, temp.ParameterValue.B, temp.ParameterValue.A)
            self.AssassinMaterial.SetVectorParameterValue(temp.ParameterName, color)
        for temp in RandomMaterial.TextureParameterValues:
            if not temp.ParameterValue is None:
                self.AssassinMaterial.SetTextureParameterValue(temp.ParameterName, temp.ParameterValue)
        for temp in RandomMaterial.ScalarParameterValues:
            self.AssassinMaterial.SetScalarParameterValue(temp.ParameterName, temp.ParameterValue)

    SkullMasherBarrel = bl2sdk.FindObject("WeaponPartDefinition", "GD_Weap_SniperRifles.Barrel.SR_Barrel_Jakobs_Skullmasher")

    def handle_zooming(self, caller, function, params):
        # Get the speed of the Player, needs to be increased while aiming
        PlayerPawn = self.get_player_controller().Pawn

        if caller.Instigator == PlayerPawn:
            if PlayerPawn.Weapon.DefinitionData.BarrelPartDefinition == self.SkullMasherBarrel:
                # Get the Current WorldInfo to set the time dilation
                WorldInfo = bl2sdk.GetEngine().GetCurrentWorldInfo()

                # 1 == Zooming in / 2 == Zoomed in / 3 == Zooming out / 0 == Not Zoomed

                # Only slow time while zooming in
                if params.NewZoomState in (1, 2):
                    WorldInfo.TimeDilation = 0.4500000
                    self.randomize_weapon_skin()

                elif params.NewZoomState == 0:
                    WorldInfo.TimeDilation = 1.0000000

            else:
                pass
        else:
            pass

    # Checks if weapon is zoomed in
    # Hooks the games SetZoomState function
    ZoomHook = "WillowGame.WillowWeapon.SetZoomState"

    def enable_slow(self):
        self.part_changes()
        bl2sdk.RegisterHook(self.ZoomHook, "ZoomHook", IsZoomingHook)

    def disable_slow(self):
        bl2sdk.RemoveHook(self.ZoomHook, "ZoomHook")

AssassinInstance = Assassin()

# This function gets called every time the player starts to change the zoom status
def is_zooming_hook(caller: bl2sdk.UObject, function: bl2sdk.UFunction, params: bl2sdk.FStruct) -> bool:
    AssassinInstance.HandleZooming(caller, function, params)
    return True

bl2sdk.Mods.append(AssassinInstance)
