#$TenantId = 'b1ab0057-c4e0-4704-b954-aec02949b6ff' #andreanldev.onmicrosoft.com
$TenantId = "f614c3e2-2493-4b3b-a84d-7ceae8753be3" #mydre.org
#$stageName = 'Tst'
$stageName = 'Andrea'
$workspaceNetworkRg = -Join ($stageName, '-', 'Workspace-Network') 
$workspaceRouteTable = 'Workspace-routes'

#$nsgpattern = 'NSG-Subnet*' #(Some Old RUMC Subs have this pattern)
$nsgpattern = 'dws*nsg*' #New subscription have this pattern
$subscription = ''
Connect-AzAccount -TenantId $TenantId
$subscription = Get-AzSubscription -TenantId $TenantId| Out-Gridview -Title 'subscriptions' -PassThru
Select-AzSubscription -subscription $subscription

# Check if the subscription has workspace networking components
$networkrg = Get-AzResourceGroup -Name $workspaceNetworkRg
if ($networkrg -eq $null)
{
    throw 'Workspace Networking Resource Group not found'
}
$workspaceNsgs = Get-AzNetworkSecurityGroup -Name $nsgpattern

$wsAddresses = @()
# Iterate over each Workspace NSG
foreach ($wsNsg in $workspaceNsgs)
{
    if ($wsNsg.Name -like '*Server*') #Ignore the WS VM NSGs
    {
        continue
    }
    else
    {
        $wsNsgConfiguration = Get-AzVirtualNetworkSubnetConfig -ResourceId $wsNsg.Subnets[0].Id
        $wsAddress = New-Object PSObject
        $wsAddress | Add-Member -MemberType NoteProperty -Name "workspace" -Value $wsNsg.ResourceGroupName.Replace('-','')
        $wsAddress | Add-Member -MemberType NoteProperty -Name "network" -Value $wsNsgConfiguration.AddressPrefix.Replace('{','').Replace('}','')
        $wsAddresses += $wsAddress
    }
}

$wsAddresses | Export-Csv c:\temp\workspaces.csv -NoTypeInformation