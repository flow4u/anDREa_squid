<#
.SYNOPSIS
    Get the myDRE insights in terms of per Subscription: Workspaces, Tenant, Creation date, #users, #vms, type of vms
.DESCRIPTION

.NOTES
    Before running the script, the command Connect-AzureAD must be ran from prompt
.LINK

.EXAMPLE

#>
# starting to get all the data
Write-Output "ws_network.ps1 started  at $(Get-Date)"

# creating file with only header
$FileName = "wsname_network2.csv"
[PSCustomObject] @{
                Tenant         = ""
                Subscription   = ""
                ResourceGroup  = ""
                Network        = ""
            } | ConvertTo-Csv | Select-Object -SkipLast 1 | Out-File -Path .\$FileName

# adding all the data without headers by looping over all subscriptions
Get-AzSubscription | ForEach-Object {
    # get the relevant information of/in a subscription
    $SubscriptionName = $_.Name
    $Tenant = "{2}" -f $SubscriptionName.Split('-')
    # setting the context for further looping
    Set-AzContext -SubscriptionId $_.SubscriptionId
    # looping over every ResourceGroup, put it in a table and append it to the file
    (Get-AzResourceGroup).ResourceGroupName | ForEach-Object {
        if ($null -ne $_) {
            # only process ResourcGroups that are Workspaces
            if($_.Contains('dws')) {
                # Get the network
                $rsg = $_ 
                $nsg = $rsg.replace('-', '') + 'nsg'
                $AddressPrefix = ''
                # # $AddressPrefix = (Get-AzNetworkSecurityGroup -Name dws1467STEFAN10nsg -ResourceGroupName dws-1467-STEFAN10 | Get-AzNetworkSecurityRuleConfig -Name AllowSubnetinbound).SourceAddressPrefix
                # try {
                #     $AddressPrefix = (Get-AzNetworkSecurityGroup -Name $nsg -ResourceGroupName $rsg | Get-AzNetworkSecurityRuleConfig -Name "AllowSubnetinbound").SourceAddressPrefix[0]
                # }
                # catch {
                #     try {
                #         $AddressPrefix = (Get-AzNetworkSecurityGroup -Name $nsg -ResourceGroupName $rsg | Get-AzNetworkSecurityRuleConfig -Name "AllowAccessibleSubnetinbound0").SourceAddressPrefix[0]
                #     }
                #     catch {
                #         $temp = (Get-AzNetworkSecurityGroup -Name NSG* -ResourceGroupName $rsg | Get-AzNetworkSecurityRuleConfig -Name "allowAccessibleSubnetinbound0")
                #         $AddressPrefix = $temp.SourceAddressPrefix
                #     } 
                # }
                try {
                    $subnet = (Get-AzNetworkSecurityGroup -Name $nsg -ResourceGroupName $rsg)
                    $AddressPrefix = (Get-AzVirtualNetworkSubnetConfig -ResourceId $subnet.Subnets[0].Id).AddressPrefix[0]
                }
                catch {
                    try {
                        $subnet = (Get-AzNetworkSecurityGroup -Name NSG* -ResourceGroupName $rsg)
                        $AddressPrefix = (Get-AzVirtualNetworkSubnetConfig -ResourceId $subnet.Subnets[0].Id).AddressPrefix[0]
                    }
                    catch {
                        $subnet = (Get-AzNetworkSecurityGroup -Name subnet* -ResourceGroupName $rsg)
                        $AddressPrefix = (Get-AzVirtualNetworkSubnetConfig -ResourceId $subnet.Subnets[0].Id).AddressPrefix[0]
                    }
                }
                # catch {
                #     $subnet = (Get-AzNetworkSecurityGroup -Name NSG* -ResourceGroupName $rsg)
                #     $AddressPrefix = (Get-AzVirtualNetworkSubnetConfig -ResourceId $subnet.Subnets[0].Id).AddressPrefix[0]
                # }
                
                # Create the row in the table
                [PSCustomObject] @{
                    Tenant         = $Tenant
                    Subscription   = $SubscriptionName
                    ResourceGroup  = $_
                    Network        = $AddressPrefix
                }     
            }
        }  
    } | ConvertTo-Csv | Select-Object -Skip 1 | Add-Content -Path .\$FileName
}
# Data is collected and saved
Write-Output "ws_network.ps1 finished at $(Get-Date)"